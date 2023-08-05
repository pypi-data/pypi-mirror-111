from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import gc
import inspect
import json
import numbers
import os
import random
import shutil
import sys
import time
import uuid

try:
    from PIL import ImageEnhance
    from PIL import ImageOps
    from PIL import ImageFilter
    from PIL import Image as pil_image
    from PIL.PngImagePlugin import PngImageFile
except ImportError:
    pil_image = None
    ImageEnhance = None
    ImageFilter = None
from functools import partial
import tempfile
import numpy as np
import torch
import torch.nn as nn

from trident import __version__
from trident.backend.common import *
from trident.backend.tensorspec import *

from trident.backend.pytorch_backend import *
from trident.backend.pytorch_ops import *
from trident.backend import model
from trident.data.mask_common import color2label
from trident.data.transform import Transform
from trident.callbacks import UnfreezeModelCallback,LambdaCallback
from trident.backend.opencv_backend import array2image, image2array

from trident.data.dataset import Iterator, NumpyDataset, LabelDataset
from trident.optims.trainers import TrainingPlan
from trident.data.data_provider import DataProvider
from trident.optims.pytorch_constraints import get_constraint
from trident.optims.pytorch_losses import *
from trident.optims.pytorch_metrics import get_metric
from trident.optims.pytorch_optimizers import get_optimizer
from trident.optims.pytorch_regularizers import get_reg
from trident.callbacks import LambdaCallback
from trident.layers.pytorch_layers import *

from trident.callbacks.lr_schedulers import get_lr_scheduler, AdjustLRCallbackBase, AdjustLRCallback
from trident.data.image_common import *
from trident import context

__all__ = ['Model', 'MuiltiNetwork', 'ImageClassificationModel', 'ImageRegressionModel', 'ImageDetectionModel', 'ImageGenerationModel',
           'ImageSegmentationModel', 'FaceLandmarkModel', 'FaceRecognitionModel', 'LanguageModel']

ctx = context._context()

working_directory = ctx.working_directory
_, term_width = get_terminal_size()
term_width = int(term_width)
TOTAL_BAR_LENGTH = 65.
last_time = time.time()
begin_time = last_time


def _to_tuple(x):
    if isinstance(x, tuple):
        return x
    elif isinstance(x, list):
        return tuple(x)
    else:
        return x,


def make_deterministic(seed: int = 19260817, cudnn_deterministic: bool = False):
    r"""Make experiment deterministic by using specific random seeds across
    all frameworks and (optionally) use deterministic algorithms.
    Args:
        seed (int): The random seed to set.
        cudnn_deterministic (bool): If `True`, set CuDNN to use
            deterministic algorithms. Setting this to `True` can negatively
            impact performance, and might not be necessary for most cases.
            Defaults to `False`.
    """

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    if cudnn_deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


class Model(model.ModelBase):
    def __init__(self, inputs=None, input_shape=None, output=None, name=None):
        super().__init__(inputs, input_shape, output, name)
        self.batch_index = 0
        self.filter_index = 1
        self._enable_tensorboard = False
        self.summary_writer = None
        self.accumulate_grads_inteval = 1

    def _initial_graph(self, inputs=None, input_shape=None, output=None, initializer=None):
        if hasattr(output, '_signature'):
            output._signature = None
        if isinstance(input_shape, numbers.Integral):
            input_shape = TensorShape([None] + [input_shape])
        elif isinstance(input_shape, (tuple, list)) and isinstance(input_shape[-1], numbers.Integral):
            input_shape = TensorShape([None] + list(input_shape))

        if output is None:
            raise ValueError('There is at least one output')
        elif isinstance(output, (np.ndarray, torch.Tensor)):
            self._model = to_tensor(output, requires_grad=True)
            self._model._signature = Signature()
            self._model._signature.outputs['output'] = TensorSpec.tensor_to_spec(self._model)
            self._model._signature.outputs['output'].object_type = ObjectType.rgb
            if inputs is None:
                self._model._signature.inputs['input'] = TensorSpec.tensor_to_spec(self._model)
                self._model._signature.inputs['input'].object_type = ObjectType.rgb
            else:
                if inputs is not None and not isinstance(inputs, (tuple, list, dict)):
                    inputs = (inputs,)

                if not isinstance(inputs, dict):
                    for i in range(len(inputs)):
                        inp = to_tensor(inputs[i])
                        output._signature.inputs['input_{0}'.format(i)] = TensorSpec.tensor_to_spec(inp, need_exclude_batch_axis=True, is_singleton=False, optional=False,
                                                                                                    name='input_{0}'.format(i))
                else:
                    for k, v in inputs.items():
                        inp = to_tensor(v)
                        output._signature.inputs[k] = TensorSpec.tensor_to_spec(inp, need_exclude_batch_axis=True, is_singleton=False, optional=False, name=k)
            self._model.signature = self._model._signature

        elif isinstance(output, (Layer, nn.Module)):
            if inputs is not None and not isinstance(inputs, (tuple, list, dict)):
                inputs = (inputs,)
            if input_shape is not None and not isinstance(input_shape, (tuple, list, dict)):
                input_shape = (input_shape,)
            if isinstance(output, Combine):
                output._signature = Signature(name=output.__class__.__name__)
                for i in range(len(inputs)):
                    output._signature.inputs['x_{0}'.format(i)] = TensorSpec(TensorShape([None]))
            else:
                output._signature = get_signature(output, output.__class__.__name__)
            if inputs is not None and len(output._signature.inputs) >= len(inputs) > 0:
                if not isinstance(inputs, dict):
                    for i in range(len(inputs)):
                        k = output._signature.inputs.key_list[i]
                        inp = to_tensor(inputs[i])
                        output._signature.inputs[k] = TensorSpec.tensor_to_spec(inp, need_exclude_batch_axis=True, is_singleton=False,
                                                                                optional=output._signature.inputs[k].optional, name=k)
                else:
                    available_items = output._signature.inputs.key_list.copy()
                    for k, v in inputs.items():
                        if k in output._signature.inputs.key_list:
                            output._signature.inputs[k] = TensorSpec.tensor_to_spec(v, need_exclude_batch_axis=True, is_singleton=False,
                                                                                    optional=output._signature.inputs[k].optional, name=k)
                            available_items.remove(k)
                        else:
                            for sk in available_items:
                                if sk.lower() == k.lower():
                                    output._signature.inputs[sk] = TensorSpec.tensor_to_spec(v, need_exclude_batch_axis=True, is_singleton=False,
                                                                                             optional=output._signature.inputs[sk].optional, name=sk)
                                    available_items.remove(sk)
                                    break

            elif input_shape is not None and len(output._signature.inputs) >= len(input_shape):
                if not isinstance(input_shape, dict):
                    for i in range(len(input_shape)):
                        k = output._signature.inputs.key_list[i]
                        output._signature.inputs[k].shape = input_shape[i] if isinstance(input_shape[i], TensorShape) else TensorShape([None] + input_shape[i])
                        output._signature.inputs[k].dtype = dtype.float32
                        for module in output.modules():
                            if isinstance(module, (Embedding, nn.Embedding)):
                                output._signature.inputs[k].dtype = dtype.int64
                                break


                else:
                    available_items = output._signature.inputs.key_list.copy()
                    for k, v in input_shape.items():
                        if k in output._signature.inputs.key_list:
                            output._signature.inputs[k].shape = TensorShape([None] + v)
                            available_items.remove(k)
                        else:
                            for sk in available_items:
                                if sk.lower() == k.lower():
                                    output._signature.inputs[sk].shape = TensorShape([None] + v)
                                    available_items.remove(sk)
                                    break

            # update notes
            output.is_root = True
            output.nodes = OrderedDict([(mod.uuid, mod) for mod in list(output.modules()) if isinstance(mod, Layer)])
            for name, mod in output.named_modules():
                if isinstance(mod, Layer):
                    mod.nodes = output.nodes
                    mod.relative_name = name
            # output.cpu()

            out = None
            if inputs is not None:
                inputs = unpack_singleton(inputs)
                args = None
                if isinstance(inputs, dict):
                    out = output(*list(inputs.values()))
                elif isinstance(inputs, (list, tuple)):
                    out = output(*inputs)
                else:
                    out = output(inputs)

            else:

                # output.input_shape = input_shape
                dummay_input = [to_tensor(shape.get_dummy_tensor()).to(get_device()) for shape in input_shape]
                # prevent pytorch 'ValueError: Expected more than 1 value per channel when training, got input size ....
                output.to(get_device())
                output.eval()
                out = output(*dummay_input)

            self._model = output
            # self._model.input_spec=TensorSpec(shape=self._model.input_shape,dtype=self._model.weights[0].data.dtype)

            if is_tensor(out) and len(output._signature.outputs) == 1:
                output._signature.outputs[output._signature.outputs.key_list[0]].shape = tensor_to_shape(out)
                output._signature.outputs[output._signature.outputs.key_list[0]].dtype = DTYPE_MAPPING[out.dtype] if out.dtype in DTYPE_MAPPING else out.dtype

            elif isinstance(out, OrderedDict):
                for k, v in out.item_list:
                    output.signature.outputs[k] = TensorSpec(shape=tensor_to_shape(v), name=k)

            elif isinstance(out, (list, tuple)):
                for i in range(len(out)):
                    output.signature.outputs['output_{0}'.format(i)] = TensorSpec(shape=tensor_to_shape(out[i]), name='output_{0}'.format(i))

        elif isinstance(output, (list, tuple)) and all([isinstance(m, (nn.Module)) for m in output]):
            output_list = []
            model_list = []
            dummay_input = to_tensor(input_shape.get_dummy_tensor()).to(get_device()) if not is_tensor(inputs) else inputs.to(get_device())

            for op in output:
                if isinstance(op, (Layer, nn.Module)):
                    op.to(get_device())
                    # prevent pytorch 'ValueError: Expected more than 1 value per channel when training, got input size ....
                    op.eval()
                    out = fix_layer(op)(dummay_input)
                    model_list.append(op)
                    output_list.extend(*out)
            model = Combine(model_list)
            self._model = model
            self.name = model.name
            for i in range(len(output_list)):
                output.signature.outputs['output_{0}'.format(i)] = TensorSpec(shape=tensor_to_shape(output_list[i]), name='output_{0}'.format(i))


        elif isinstance(output, (np.ndarray, torch.Tensor)):
            pass

        else:
            raise ValueError('Invalid output')

        self.training_context['current_model'] = self._model
        if not hasattr(self._model, 'name'):
            self._model._name = 'model_' + str(uuid.uuid4().node)
        if self.save_path is None:
            save_path = os.path.join('Models', '{0}.pth.tar_'.format(self._model._name))
            self.save_path = sanitize_path(make_dir_if_need(save_path))
        else:
            self.save_path = sanitize_path(make_dir_if_need(self.save_path))
        self.training_context['save_path'] = self.save_path

    @property
    def device(self):
        return get_device()

    def train(self):
        if self._model is not None and isinstance(self._model, torch.Tensor):
            pass
        elif self._model is not None and isinstance(self._model, nn.Module) and self._model.built:
            self._model.train()
        else:
            raise ValueError('There is no built model ,nothing to learn')

    def eval(self):
        if self._model is not None and isinstance(self._model, torch.Tensor):
            pass
        elif self._model is not None and isinstance(self._model, Layer) and self._model.built:
            self._model.eval()
        else:
            raise ValueError('There is no built model ,nothing to evaluate')

    @property
    def layers(self):
        if self._model is not None and isinstance(self._model, Layer):
            return self._model.nodes
        else:
            return []

    def complie(self, optimizer="Adam",
                loss=None,
                metrics=None,
                loss_weights=None,
                **kwargs
                ):
        self.with_optimizer(optimizer, lr=2e-3, betas=(0.9, 0.999))
        if loss is not None:
            if isinstance(loss, str) or callable(loss) or inspect.isfunction(loss) or inspect.isclass(loss):
                loss_weights = 1.0 if loss_weights is None or not isinstance(loss, numbers.Number) else loss_weights
                self.with_loss(loss, loss_weight=loss_weights)
            elif isinstance(loss, list):
                if loss_weights is not None and isinstance(loss_weights, list) and len(loss_weights) == len(loss):
                    for k in range(len(loss)):
                        loss_item = loss[k]
                        weight = loss_weights[k] if isinstance(loss_weights[k], numbers.Number) else 1.0
                        self.with_loss(loss_item, loss_weight=weight)
                else:
                    for loss_item in loss:
                        self.with_loss(loss_item)

            elif isinstance(loss, dict):
                if loss_weights is not None and isinstance(loss_weights, dict):
                    for k, v in loss.items():
                        if k in loss_weights:
                            weight = loss_weights[k] if isinstance(loss_weights[k], numbers.Number) else 1.0
                            self.with_loss(v, loss_weight=weight, name=k)
                        else:
                            self.with_loss(v, loss_weight=1.0, name=k)
                else:
                    for k, v in loss.items():
                        self.with_loss(v, loss_weight=1., name=k)
        if metrics is not None:
            if isinstance(metrics, str) or callable(metrics) or inspect.isfunction(metrics) or inspect.isclass(metrics):
                self.with_metric(metrics)
            elif isinstance(metrics, list):
                for metric in metrics:
                    self.with_metric(metric)
            elif isinstance(metrics, dict):
                for k, v in metrics.items():
                    self.with_metric(v, name=k)
        return self

    def fit(self,
            x=None,
            y=None,
            batch_size=8,
            epochs=1,
            verbose=1,
            callbacks=None,
            validation_split=0.0,
            validation_data=None,
            shuffle=True,
            class_weight=None,
            sample_weight=None,
            initial_epoch=0,
            steps_per_epoch=None,
            validation_steps=None,
            validation_batch_size=8,
            validation_freq=1,
            max_queue_size=10,
            workers=1,
            use_multiprocessing=False,
            ):

        split_range = list(range(len(x)))
        random.shuffle(split_range)
        cutoff = int(validation_split * len(x))
        mask_validate = split_range[:cutoff]
        mask_train = split_range[cutoff:]
        train_x = x[mask_train]
        train_y = y[mask_train]
        validate_x = x[mask_validate]
        validate_y = y[mask_validate]

        data_ds = NumpyDataset(data=train_x, symbol="input")
        label_ds = LabelDataset(labels=train_y, symbol="target")
        dataprovider = DataProvider(traindata=Iterator(data=data_ds, label=label_ds, minibatch_size=batch_size, is_shuffe=shuffle, buffer_size=max_queue_size, workers=workers))
        if validation_split > 0:
            data_test_ds = NumpyDataset(data=train_x, symbol="input")
            label_test_ds = LabelDataset(labels=train_y, symbol="target")
            dataprovider.testdata = Iterator(data=data_test_ds, label=label_test_ds, minibatch_size=validation_batch_size, is_shuffe=shuffle, buffer_size=max_queue_size,
                                             workers=workers)

        plan = TrainingPlan() \
            .add_training_item(self) \
            .with_data_loader(dataprovider) \
            .repeat_epochs(epochs) \
            .within_minibatch_size(batch_size) \
            .print_progress_scheduling(1, unit='epoch') \
            .out_sample_evaluation_scheduling(validation_steps, unit='epoch') \
            .save_model_scheduling(1, unit='epoch').start_now()
        return self

    def with_optimizer(self, optimizer, **kwargs):
        params = [self._model] if is_tensor(self._model) else self._model.parameters()
        if isinstance(optimizer, str):
            optimizer_class = get_optimizer(optimizer)
            self.optimizer = optimizer_class(params, **kwargs)
        else:
            self.optimizer = optimizer(params, **kwargs)

        self.base_lr = kwargs.get('lr', kwargs.get('learning_rate', 1e-3))
        self.training_context['current_lr'] = self.base_lr
        return self

    def with_loss(self, loss, loss_weight=1, start_epoch=0, name='', **kwargs):
        alias = name
        argnames = Signature()
        if (alias is None or len(alias) == 0) and hasattr(loss, '__name__'):
            alias = loss.__name__

        if isinstance(loss, str):
            if loss == 'output':
                self.use_output_as_loss = True
                return self
            else:
                loss_class = get_loss(loss)
                alias = loss if loss_class is not None else alias
                # loss can add mutiple times.
                if alias in self._losses:
                    dup_keys = [key for key in self._losses.key_list if alias + '_' in key]
                    alias = alias + '_' + str(len(dup_keys) + 1)
                self._losses[alias] = loss_class(**kwargs) if len(kwargs) > 0 else loss_class()

        elif inspect.isclass(loss) and loss.__class__.__name__ == "type":  # The loss is a class but not initialized yet.
            alias = loss.__class__.__name__ if alias is None or len(alias) == 0 else alias
            if alias in self._losses:
                dup_keys = [key for key in self._losses.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)

            self._losses[alias] = loss(**kwargs) if len(kwargs) > 0 else loss()


        elif not inspect.isfunction(loss) and callable(loss):  # The loss is a class and initialized yet.
            alias = loss.__class__.__name__ if alias is None or len(alias) == 0 else alias
            if alias in self._losses:
                dup_keys = [key for key in self._losses.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            self._losses[alias] = loss

        elif inspect.isfunction(loss):
            if alias in self._losses:
                dup_keys = [key for key in self._losses.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            spec = inspect.getfullargspec(loss)
            if len(spec.args) >= 2 and len(spec.args) - 0 if spec.defaults is None else len(spec.defaults) == 2:
                self._losses[alias] = loss
            else:
                self._losses[alias] = partial(loss, **kwargs)
        args = get_signature(loss, alias)
        for k, v in kwargs.items():
            if k in args.inputs and v is not None:
                args.inputs[k].default = v
        self._losses[alias].signature = args
        print(self._losses[alias].signature)

        self.loss_weights[alias] = float(loss_weight)
        self._losses[alias].__name__ = alias
        # self._losses[alias].signature = argnames
        self._losses[alias].start_epoch = start_epoch

        return self

    def with_metric(self, metric, print_only=False, name='', **kwargs):

        alias = name
        argnames = OrderedDict()
        if (alias is None or len(alias) == 0) and hasattr(metric, '__name__'):
            alias = metric.__name__

        if isinstance(metric, str):
            alias = metric if len(alias) == 0 else alias
            metric_fn = get_metric(metric)
            if alias in self._metrics:
                dup_keys = [key for key in self._metrics.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            self._metrics[alias] = metric

        elif inspect.isclass(metric) and metric.__class__.__name__ == "type":
            alias = metric.__class__.__name__ if len(alias) == 0 else alias
            if alias in self._metrics:
                dup_keys = [key for key in self._metrics.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            self._metrics[alias] = metric(**kwargs) if len(kwargs) > 0 else metric()
        elif not inspect.isfunction(metric) and callable(metric):
            alias = metric.__class__.__name__ if len(alias) == 0 else alias
            if alias in self._metrics:
                dup_keys = [key for key in self._metrics.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            self._metrics[alias] = metric
        elif inspect.isfunction(metric):
            if alias in self._metrics:
                dup_keys = [key for key in self._metrics.key_list if alias + '_' in key]
                alias = alias + '_' + str(len(dup_keys) + 1)
            self._metrics[alias] = metric
        args = get_signature(metric, alias)

        for k in kwargs.keys():
            if k in args.inputs and kwargs.get(k) is not None:
                pass
            else:
                kwargs.pop(k)
        if len(kwargs) > 0:
            self._metrics[alias] = partial(metric, **kwargs)
        self._metrics[alias].signature = args
        print(self._metrics[alias].signature)
        self._metrics[alias].__name__ = alias
        # self._metrics[alias].signature = argnames
        self._metrics[alias].print_only = print_only
        return self

    def with_regularizer(self, reg, reg_weight=None, **kwargs):
        if reg is None:
            return self
        reg_fn = None
        if isinstance(reg, str):
            reg_fn = get_reg(reg)
        elif reg is callable or inspect.isfunction(reg):
            reg_fn = reg

        reg_weight = kwargs.get('reg_weight', reg_weight)
        if 'reg_weight' in kwargs:
            kwargs.pop('reg_weight')

        args = get_signature(reg_fn)
        if reg_weight is not None:
            args.inputs['reg_weight'].default = reg_weight

        self._regs[reg_fn.__name__] = reg_fn
        self._regs[reg_fn.__name__].signature = args
        return self

    def with_constraint(self, constraint, **kwargs):
        if constraint is None:
            return self
        constraint_fn = None
        if isinstance(constraint, str):
            constraint_fn = get_constraint(constraint)

        if hasattr(constraint_fn, 'forward') and constraint_fn.__name__[-4:] == 'norm':
            self._constraints[constraint_fn.__name__] = constraint_fn(**kwargs)

        elif callable(constraint_fn) and constraint_fn.__name__[-4:] == 'norm':
            self._constraints[constraint_fn.__name__] = partial(constraint_fn, **kwargs)

        return self

    def with_initializer(self, initializer, **kwargs):
        self.initializer = initializer
        if self._model is not None and isinstance(self._model, Layer) and self._model._built:
            self.initializer(self._model, **kwargs)
        return self

    def with_model_save_path(self, save_path, **kwargs):
        if save_path is None or len(save_path) == 0:
            save_path = os.path.join('Models', '{0}.pth.tar_'.format(self.name))
        save_path = sanitize_path(save_path)
        make_dir_if_need(save_path)
        self.training_context['save_path'] = save_path
        return self

    def with_learning_rate_scheduler(self, lr_schedule, warmup=0, **kwargs):
        if lr_schedule is None:
            return self
        if isinstance(lr_schedule, str):
            lr_schedule = get_lr_scheduler(lr_schedule)

        if callable(lr_schedule):
            lr_scheduler = lr_schedule(**kwargs)
            self.callbacks.append(lr_scheduler)
        elif isinstance(lr_schedule, AdjustLRCallbackBase):
            self.callbacks.append(lr_schedule)
        self.warmup = warmup
        if self.warmup > 0:
            self.optimizer.adjust_learning_rate(1e-6, False)
            self.training_context['current_lr'] = 1e-6
        return self

    def with_automatic_mixed_precision_training(self, **kwargs):
        """Enable automatic mixed precision training
            only enable when using pytorch 1.6 (or higher) as backend and cuda is available.

        Args:
            **kwargs ():

        Returns:
            the model self

        """
        if ctx.amp_available:
            self.is_autocast_enabled = True
            self.gradscaler = torch.cuda.amp.GradScaler()
            sys.stdout.write('Automatic Mixed Precision:{0}.\n'.format('Turn On'))
        else:
            print('automatic mixed precision training only enable when using pytorch 1.6 (or higher) as backend and cuda is available.')

        return self

    def with_grad_clipping(self, clipping_threshold=3.0, **kwargs):
        """Enable grad clipping


        Args:
            clipping_threshold ():
            **kwargs ():

        Returns:
            the model self

        """
        self.grad_clipping_by_norm = True
        self.grad_clipping_threshold = clipping_threshold
        return self

    def adjust_learning_rate_scheduling(self, index: int, unit='batch', new_value: float = None):
        callback = AdjustLRCallback(index, unit, new_value)
        callback.is_shared = False
        self.callbacks.append(callback)
        return self

    def adjust_learning_rate(self, lr):
        self.optimizer.param_groups[0]['lr'] = lr
        self.training_context['current_lr'] = lr

    def do_on_epoch_start(self):
        super().do_on_epoch_start()
        if self.training_context['steps'] == 0:
            self.training_context['time_epoch_start'] = time.time()
            self.training_context['time_epoch_progress'] = 0

    def do_on_epoch_end(self):
        super().do_on_epoch_end()
        if self.model is not None and self.model.device == 'cuda':
            torch.cuda.synchronize()
            torch.cuda.empty_cache()
            gc.collect()
        if self.optimizer is not None:
            if self.warmup > 0 and self.training_context['current_epoch'] + 1 < self.warmup:
                lr = 1e-6 * (self.training_context['current_epoch'] + 1)
                self.optimizer.adjust_learning_rate(self.base_lr, verbose=True)
                self.training_context['current_lr'] = lr
            elif 0 < self.warmup == self.training_context['current_epoch'] + 1:
                self.optimizer.adjust_learning_rate(self.base_lr, verbose=True)
                self.training_context['current_lr'] = self.base_lr

    def do_on_batch_start(self):
        super().do_on_batch_start()
        if self.training_context['steps'] == 0:
            self.training_context['time_batch_progress'] = 0
            self.training_context['time_epoch_progress'] = 0
        self.training_context['time_batch_start'] = time.time()

        if (self.training_context['steps'] + 1) % 100 == 0:
            if self.model.device == 'cuda':
                torch.cuda.synchronize()
                torch.cuda.empty_cache()
                gc.collect()

    def do_on_batch_end(self):
        super().do_on_batch_end()
        self.training_context['time_batch_end'] = time.time()
        self.training_context['time_batch_progress'] += (self.training_context['time_batch_end'] - self.training_context['time_batch_start'])
        self.training_context['time_epoch_progress'] += (self.training_context['time_batch_end'] - self.training_context['time_batch_start'])
        if (self.training_context['steps'] + 1) % ctx.epoch_equivalent == 0:
            if self.warmup > 0 and self.warmup == (self.training_context['steps'] + 1) // ctx.epoch_equivalent:
                self.adjust_learning_rate(self.training_context['base_lr'])
                self.warmup = 0
        if self.training_context['current_batch'] == 0:
            temp = OrderedDict()
            for k in self.training_context['losses'].key_list:
                if k != 'epoch' and len(self.training_context['losses'][k]) > 0:
                    temp[k] = self.training_context['losses'][k][-1][-1]
            temp['total_losses'] = to_numpy(self.training_context['current_loss'])[0]
            print('{ ' + ', '.join(['{0}: {1}'.format(k, adaptive_format(v, value_type='loss')) for k, v in temp.items()]) + ' }')

    def do_on_data_received(self, train_data, test_data):

        # fields=train_data._fields
        # for i in range(len(fields)):
        if train_data is None and test_data is None:
            return self.training_context['train_data'], self.training_context['test_data']
        if self.training_context['steps'] == 0 and ('data_feed' not in self.training_context or len(self.training_context['data_feed']) == 0 or len(
                [v for v in self.training_context['data_feed'].value_list if v is None]) > 0):
            try:
                data_feed = OrderedDict() if 'data_feed' not in self.training_context else self.training_context['data_feed']
                if isinstance(self._model, Layer):

                    inshapes = self.inputs.value_list
                    outshapes = self.targets.value_list
                    available_fields = copy.deepcopy(train_data.key_list)
                    if train_data is not None:
                        # check input
                        for arg in self._model.signature.inputs.key_list:
                            if arg in data_feed and data_feed[arg] in available_fields:
                                available_fields.remove(data_feed[arg])
                            else:
                                data_feed[arg] = ''
                                if len(train_data) == 1 and len(self._model.signature.inputs.key_list) == 1:
                                    data_feed[arg] = train_data.key_list[0]
                                    available_fields.remove(train_data.key_list[0])
                                elif arg in available_fields:
                                    data_feed[arg] = arg
                                    available_fields.remove(arg)
                                elif arg in ['x', 'input'] and 'data' in available_fields:
                                    data_feed[arg] = 'data'
                                    available_fields.remove('data')
                                elif arg in ['x', 'input'] and 'image' in available_fields:
                                    data_feed[arg] = 'image'
                                    available_fields.remove('image')
                                elif arg == 'x' and 'input' in available_fields:
                                    data_feed[arg] = 'input'
                                    available_fields.remove('input')
                                elif len(self._model.signature.inputs.key_list) == 1:
                                    for item in available_fields:
                                        data_shape = train_data[item].shape if len(train_data[item].shape) > 2 else TensorShape([None])
                                        if 'target' not in item and 'output' != item and data_shape == inshapes[0].shape:
                                            data_feed[arg] = item
                                            available_fields.remove(item)
                                            break
                                else:
                                    Warning(
                                        'input argment {0} cannot mapping to any data, please check it and update the datafeed'.format(
                                            arg))

                        # check for target
                        if len(available_fields) > 0:
                            if len(available_fields) == 1:
                                data_feed['target'] = available_fields[0]
                            else:
                                for i in range(len(self.targets)):
                                    arg = self.targets.key_list[i]
                                    data_feed[arg] = ''
                                    if len(train_data) == 1:
                                        data_feed[self.targets.key_list[0]] = train_data.key_list[0]
                                    elif arg in available_fields:
                                        data_feed[arg] = arg
                                        available_fields.remove(arg)
                                    elif arg == 'target' and 'label' in available_fields:
                                        data_feed[arg] = 'label'
                                        available_fields.remove('label')
                                    elif arg == 'target' and len(available_fields) == 1:
                                        data_feed[arg] = available_fields[0]
                                        available_fields.remove(available_fields[0])
                                    elif len(available_fields) > 0:
                                        target_shape = outshapes
                                        for item in available_fields:
                                            data_shape = list(train_data[item].shape) if len(train_data[item].shape) > 1 else [None]
                                            if target_shape == data_shape:
                                                data_feed[arg] = item
                                                available_fields.remove(item)
                                            elif ('int64' in str(train_data[item].dtype) or 'int32' in str(
                                                    train_data[item].dtype)) and target_shape[:-1] == data_shape:
                                                data_feed[arg] = item
                                                available_fields.remove(item)
                                            else:
                                                Warning(
                                                    'target argment {0} cannot mapping to any data, please check it and update the datafeed'.format(
                                                        arg))
                                # if len(self.targets) == 1 and data_feed[self.targets.key_list[0]] != None:
                                #     self.training_context['current_target'] = train_data[data_feed[self.targets.key_list[0]]]

                        # if len(self._signature.inputs.key_list) == 1 and data_feed[self._signature.inputs.key_list[0]] != None:
                        #     self.training_context['data_feed'] = data_feed
                        # elif '' not in data_feed.value_list:
                        self.training_context['data_feed'] = data_feed
                        print('data_feed for {0} :'.format(self.name))
                        print(json.dumps(data_feed, indent=4, sort_keys=True))

            except:
                PrintException()

        # convert to tensor
        try:
            data_feed = self.training_context['data_feed']
            input_list = [data_feed[arg] for arg in self._model.signature.inputs.key_list]
            for item in train_data.key_list:
                train_data[item] = to_tensor(train_data[item], device=get_device())
                if item in input_list and 'float' in str(train_data[item].dtype):
                    train_data[item].require_grads = True

                if test_data is not None and item in test_data:
                    test_data[item] = to_tensor(test_data[item], device=get_device())  # .cpu()

            self.training_context['train_data'] = train_data
            self.training_context['test_data'] = test_data

        except:
            PrintException()
        train_data, test_data = super().do_on_data_received(self.training_context['train_data'], self.training_context['test_data'])
        self.training_context['train_data'] = train_data
        self.training_context['test_data'] = test_data
        return train_data, test_data

    def get_current_loss(self):
        return self.training_context['current_loss']

    def do_gradient_update(self, log_gradients=False):
        try:
            accumulate_grads = self.training_context['steps'] % self.accumulation_steps != 0
            need_backward = self.training_context['stop_update'] == 0 or (0 < self.training_context['stop_update'] < 1 and random.random() <= self.training_context['stop_update'])
            is_layer = isinstance(self._model, (Layer, nn.Module))

            if is_layer:
                self._model.train()
            if need_backward:
                if ctx.amp_available and self.is_autocast_enabled == True and get_device() == 'cuda':
                    if self.gradscaler is None:
                        self.gradscaler = torch.cuda.amp.GradScaler()
                    self.gradscaler.scale(self.training_context['current_loss'] / self.accumulation_steps).backward(retain_graph=self.training_context['retain_graph'])

                else:

                    (self.training_context['current_loss'] / self.accumulation_steps).backward(retain_graph=self.training_context['retain_graph'])

                # only check once every epoch start.
                if is_layer and self.grad_clipping_by_norm:

                    if ctx.amp_available and self.is_autocast_enabled == True and get_device() == 'cuda':
                        torch.nn.utils.clip_grad_norm_(self._model.parameters(), self.grad_clipping_threshold)

                    else:
                        torch.nn.utils.clip_grad_norm_(self._model.parameters(), self.grad_clipping_threshold)

                if not accumulate_grads:
                    super().on_optimization_step_start()
                    # amp support
                    if ctx.amp_available and self.is_autocast_enabled == True and get_device() == 'cuda':
                        self.gradscaler.unscale_(self.optimizer)
                        self.gradscaler.step(self.optimizer)
                        self.gradscaler.update()
                    else:
                        self.optimizer.step(self.get_current_loss)

                    self.optimizer.zero_grad()
                    if is_tensor(self._model):
                        pass
                        # if self._model.grad is not None:
                        #     self._model.requires_grad = False
                        #     self._model.requires_grad = True
                    elif is_layer:
                        self._model.zero_grad()

                    self.do_on_optimization_step_end()

            else:
                self.training_context['stop_update'] = self.training_context['stop_update'] - 1 if self.training_context['stop_update'] > 1 else self.training_context[
                    'stop_update']
                if not self.training_context['retain_graph'] and not accumulate_grads:
                    if is_layer:
                        self._model.zero_grad()
                if accumulate_grads:
                    if ctx.amp_available and self.is_autocast_enabled == True and get_device() == 'cuda':
                        if self.gradscaler is None:
                            self.gradscaler = torch.cuda.amp.GradScaler()
                        self.gradscaler.scale(self.training_context['current_loss'] / self.accumulation_steps).backward(retain_graph=self.training_context['retain_graph'])

                    else:
                        (self.training_context['current_loss'] / self.accumulation_steps).backward(retain_graph=self.training_context['retain_graph'])

        except Exception as e:
            print(e)
            PrintException()

    def do_on_optimization_step_end(self):
        super().do_on_optimization_step_end()
        self.training_context['losses'].collect('total_losses', self.training_context['steps'], to_scalar(self.training_context['current_loss']))

    def do_on_excution_exception(self):
        super().do_on_excution_exception()
        self.save_model()

    def log_gradient(self, grads=None):
        grad_dict = OrderedDict()
        if isinstance(self._model, nn.Module):
            for i, (k, v) in enumerate(self._model.named_parameters()):
                grad_dict[k] = to_numpy(v.grad)
            self.gradients_history.append(grad_dict)

    def log_weight(self, weghts=None):
        weight_dict = OrderedDict()
        if isinstance(self._model, nn.Module):
            for k, v in self._model.named_parameters():
                weight_dict[k] = to_numpy(v.data)

            self.weights_history.append(weight_dict)

    def save_model(self, save_path=None, **kwargs):
        is_abnormal = False
        for callback in self.training_context['callbacks']:
            callback.on_model_saving_start(self.training_context)

        if isinstance(self._model, Layer) and any_abnormal_number(self._model):
            is_abnormal = True
            for para in self._model.parameters():
                if any_abnormal_number(para):
                    para.data.copy_(where(is_abnormal_number(para), random_normal_like(para, mean=0, std=0.02).to(get_device()), para))
        if is_tensor(self._model) and any_abnormal_number(self._model):
            is_abnormal = True

            sys.stderr.write(self._get_name() + '  nan detected!!\n')
        if save_path is not None:
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filename = self.name
            self.training_context['save_path'] = save_path
        else:
            save_path = self.training_context['save_path']

        if isinstance(self._model, nn.Module) and not is_abnormal:
            try:
                folder, filename, ext = split_path(save_path)
                if filename == '':
                    filename = self.name

                ext = '.pth.tar'
                save_path = os.path.join(folder, filename + ext)
                make_dir_if_need(sanitize_path(save_path))
                save_path = sanitize_path(save_path)
                device = get_device()
                self._model.eval()
                self._model.cpu()
                tempfd, temppath = tempfile.mkstemp(prefix=filename, suffix=ext)
                _, tempfile_name, tempext = split_path(temppath)
                move_path = os.path.join(folder, tempfile_name + tempext)
                try:
                    torch.save({
                        'state_dict': self._model.state_dict(),
                        'backend': 'pytorch',
                        'trident_version': __version__,
                        'pytorch_version': torch.__version__,
                        'signature': self._model.signature
                    }, temppath)
                    os.close(tempfd)
                    shutil.move(temppath, move_path)
                    if os.path.exists(save_path):
                        os.remove(save_path)
                    os.rename(move_path, save_path)

                except:
                    if not os.path.exists(save_path):
                        if os.path.exists(move_path):
                            os.rename(move_path, save_path)
                        elif os.path.exists(temppath):
                            shutil.move(temppath, save_path)

                save_path = save_path.replace('.pth.tar', '.pth')
                tempfd2, temppath2 = tempfile.mkstemp(prefix=filename, suffix='.pth')
                _, tempfile2_name, tempext2 = split_path(temppath2)
                move_path2 = os.path.join(folder, tempfile2_name + tempext2)
                try:
                    save(self._model, temppath2)
                    os.close(tempfd2)
                    shutil.move(temppath2, move_path2)
                    if os.path.exists(save_path):
                        os.unlink(save_path)
                    os.rename(move_path2, save_path)

                except:
                    if not os.path.exists(save_path):
                        if os.path.exists(move_path2):
                            os.rename(move_path2, save_path)
                        elif os.path.exists(temppath2):
                            shutil.move(temppath2, save_path)

                self._model.to(get_device())
                self._model.train()

            except Exception as e:
                self._model.train()
                print(e)
                PrintException()

        elif is_tensor(self._model) and not is_abnormal:
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filenam = self.name

            ext = '.npy'
            save_path = os.path.join(folder, filename + ext)
            make_dir_if_need(sanitize_path(save_path))
            save_path = sanitize_path(save_path)
            tempfd, temppath = tempfile.mkstemp(prefix=filename, suffix=ext)
            _, tempfile_name, tempext = split_path(temppath)
            move_path = os.path.join(folder, tempfile_name + tempext)
            try:
                numpy_model = to_numpy(self._model)
                np.save(temppath, numpy_model)
                os.close(tempfd)
                shutil.move(temppath, move_path)
                if os.path.exists(save_path):
                    os.remove(save_path)
                os.rename(move_path, save_path)
            except:
                if not os.path.exists(save_path):
                    if os.path.exists(move_path):
                        os.rename(move_path, save_path)
                    elif os.path.exists(temppath):
                        shutil.move(temppath, save_path)

            np.save(save_path, numpy_model)

            sys.stdout.write('Yor model is a Tensor not a nn.Module, it has saved as numpy array(*.npy) successfully. ')
        else:
            raise ValueError('only Layer or nn.Module as model can export to onnx, yours model is {0}'.format(type(self._model)))

        for callback in self.training_context['callbacks']:
            callback.on_model_saving_end(self.training_context)

    def save_onnx(self, save_path=None, dynamic_axes=None, **kwargs):
        if isinstance(self._model, nn.Module):

            import_or_install('torch.onnx')
            self._model.eval()

            dummy_input = (to_tensor(self.signature.inputs.value_list[0].shape.get_dummy_tensor()))
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filenam = self.name

            ext = '.onnx_'
            save_path = os.path.join(folder, filename + ext)
            make_dir_if_need(sanitize_path(save_path))
            save_path = sanitize_path(save_path)

            outputs = self._model(dummy_input)
            if dynamic_axes is None:
                # dynamic_axes = {self.inputs.key_list[0]: [0],  # variable lenght axes
                #                 self.outputs.key_list[0]: [0]}
                dynamic_axes = {self.inputs.key_list[0]: {0: 'batch'}, self.outputs.key_list[0]: {0: 'batch'}}

            # dynamic_axes = {}
            #
            # for inp in self.inputs.key_list:
            #     dynamic_axes[inp] = [0]
            # for out in self.outputs.key_list:
            #     dynamic_axes[out] = [0]
            tempfd, temppath = tempfile.mkstemp(prefix=filename, suffix='.onnx')
            _, tempfile_name, tempext = split_path(temppath)
            move_path = os.path.join(folder, tempfile_name + tempext)
            try:
                with torch.no_grad():
                    with torch.cuda.amp.autocast(enabled=False):
                        torch.onnx.export(self._model,  # model being run
                                          dummy_input,  # model input (or a tuple for multiple inputs)
                                          temppath,  # where to save the model (can be a file or file-like object)
                                          export_params=True,  # store the trained parameter weights inside the model file
                                          opset_version=11,  # the ONNX version to export the model to
                                          do_constant_folding=False,  # whether to execute constant folding for optimization
                                          input_names=self.signature.inputs.key_list,  # the model's input names
                                          keep_initializers_as_inputs=True,
                                          output_names=self.signature.outputs.key_list,  # the model's output names
                                          dynamic_axes=dynamic_axes)
                os.close(tempfd)
                shutil.move(temppath, move_path)
                if os.path.exists(save_path):
                    os.remove(save_path)
                os.rename(move_path, save_path)
                self._model.train()
            except:
                if not os.path.exists(save_path):
                    if os.path.exists(move_path):
                        os.rename(move_path, save_path)
                    elif os.path.exists(temppath):
                        shutil.move(temppath, save_path)
                if os.path.exists(temppath):
                    os.remove(temppath)

            import onnx
            from onnx import shape_inference
            onnx.save(shape_inference.infer_shapes(onnx.load(save_path.replace('.onnx_', '.onnx'))), save_path.replace('.onnx_', '.onnx'))
            os.remove(save_path)
            for callback in self.training_context['callbacks']:
                callback.on_model_saving_end(self.training_context)
        else:
            raise ValueError('only Layer or nn.Module as model can export to onnx, yours model is {0}'.format(type(self._model)))

    def load_model(self, file_path, **kwargs):
        print('Loading pretrained model from {}'.format(file_path))
        folder, filename, ext = split_path(file_path)
        if filename == '':
            filename = self.name
        state_dict = None
        pretrained_dict = None
        if ext == '.pth.tar':
            state_dict = torch.load(file_path, map_location=torch.device(get_device()))
        elif ext == '.pth':
            load_path = file_path
            if not os.path.exists(file_path):
                if os.path.exists(file_path.replace(ext, '.pth.tar')):
                    load_path = file_path.replace(ext, '.pth.tar')
                elif os.path.exists(os.path.join(working_directory, filename + ext)):
                    load_path = os.path.join(working_directory, filename + ext)
            recovery_pth = torch.load(load_path, map_location=torch.device(get_device()))

            if isinstance(recovery_pth, dict):
                state_dict = recovery_pth

            elif isinstance(recovery_pth, Layer):
                state_dict = recovery_pth.state_dict()

        if 'backend' in state_dict and state_dict['backend'] != 'pytorch':
            raise RuntimeError(
                'The model archive {0} is a {1}-based model, but current backend is PyTorch, so cannot load model properly.'.format(file_path, state_dict['backend']))

        if "state_dict" in state_dict.keys():
            pretrained_dict = state_dict['state_dict']
        else:
            pretrained_dict = state_dict

        if isinstance(self._model, Layer):
            if check_keys(self._model, pretrained_dict):
                has_abnormal = False
                for key in pretrained_dict.keys():
                    value = pretrained_dict[key]
                    if is_tensor(value) and any_abnormal_number(value):
                        has_abnormal = True
                        print('detect abnormal in state_dict[{0}],value:{1}'.format(key), value)
                        pretrained_dict[key] = where(is_nan(value), random_normal_like(value, mean=0, std=0.02).to(get_device()).cast(value.dtype), value)
                    if is_tensor(value) and ndim(value) == 0:
                        pretrained_dict[key] = to_tensor(value.item())

                if has_abnormal:
                    sys.stderr.write(self._model._name + '  has_abnormal detected and  fixed!!\n')
                self._model.load_state_dict(pretrained_dict, strict=False)
                print('Model loaded!')
                # must switch to evluate first beforeinference or training
                # Dropout and Batch normalization will behavior change!!!

                self._model.eval()
        if "signature" in state_dict.keys() and (self._model.signature is None or state_dict['signature'] != self._model.signature):
            self._model.signature = state_dict['signature']
        self._model.to(get_device())

    def summary(self):
        # self.rebinding_input_output(self._model.input_shape)

        summary(self._model, [item for item in self._model._signature.inputs.value_list])
        return self

    def predict(self, input):
        if isinstance(self._model, Layer):
            self._model.eval()

    def test(self, input, target):
        raise NotImplementedError

    #
    # @property
    # def preprocess_flow(self):
    #     return self._preprocess_flow
    #
    # @preprocess_flow.setter
    # def preprocess_flow(self, value):
    #     self._preprocess_flow = value

    #
    # @property
    # def reverse_preprocess_flow(self):
    #     return_list = [reverse_image_backend_adaption]
    #     for i in range(len(self._preprocess_flow)):
    #         fn = self._preprocess_flow[-1 - i]
    #         if (inspect.isfunction(fn) and fn.__qualname__ == 'normalize.<locals>.img_op') or (isinstance(fn, Normalize) and fn.name == 'normalize'):
    #             return_list.append(Unnormalize(fn.mean, fn.std))
    #     return_list.append(array2image)
    #     return return_list

    # def data_preprocess(self, img_data):
    #     if not hasattr(self, '_preprocess_flow') or self._preprocess_flow is None:
    #         self._preprocess_flow = []
    #     if img_data.ndim == 4:
    #         return to_tensor(to_numpy([self.data_preprocess(im) for im in img_data]))
    #     if len(self._preprocess_flow) == 0:
    #         return image_backend_adaption(img_data)
    #     if isinstance(img_data, np.ndarray):
    #         for fc in self._preprocess_flow:
    #             if self._model is not None and self.signature is not None and len(self.signature) > 1 and self.input_spec is not None:
    #                 img_data = fc(img_data, spec=self.input_spec)
    #             else:
    #                 img_data = fc(img_data)
    #         img_data = image_backend_adaption(img_data)
    #         if self.input_spec is None:
    #             self.input_spec = TensorSpec(shape=tensor_to_shape(to_tensor(img_data), need_exclude_batch_axis=False), object_type=ObjectType.rgb, name='input')
    #
    #         return img_data
    #     else:
    #         return img_data
    #
    # def reverse_data_preprocess(self, img_data: np.ndarray):
    #     if img_data.ndim == 4:
    #         return to_numpy([self.reverse_data_preprocess(im) for im in img_data])
    #     if len(self.reverse_preprocess_flow) == 0:
    #         return reverse_image_backend_adaption(img_data)
    #     if isinstance(img_data, np.ndarray):
    #         # if img_data.ndim>=2:
    #         for fc in self.reverse_preprocess_flow:
    #             img_data = fc(img_data)
    #         img_data = reverse_image_backend_adaption(img_data)
    #     return img_data

    def extra_repr(self):
        return ''

    def __str__(self):
        self.__repr__()

    def _get_name(self):
        return self.__class__.__name__

    def __repr__(self):
        # We treat the extra repr like the sub-module, one item per line
        extra_lines = []
        extra_repr = self.extra_repr()
        # empty string will be split into list ['']
        if extra_repr:
            extra_lines = extra_repr.split('\n')
        child_lines = []
        for key, value in self.__dict__.items():
            try:
                if isinstance(value, OrderedDict):
                    for subkey, subvalue in value.items():
                        mod_str = repr(subvalue) if sys.getsizeof(subvalue) <= 1000000 else '<large item>'
                        mod_str = addindent(mod_str, 2)
                        child_lines.append('(' + key + '): ' + mod_str)
                else:
                    pass
                    # mod_str = repr(value) if sys.getsizeof(value)<=1000000 else '<large item>'
                    # mod_str = addindent(mod_str, 2)
                    # child_lines.append('(' + key + '): ' + mod_str)
            except:
                pass
        lines = extra_lines + child_lines

        main_str = self._get_name() + '('
        if lines:
            # simple one-liner info, which most builtin Modules will use
            if len(extra_lines) == 1 and not child_lines:
                main_str += extra_lines[0]
            else:
                main_str += '\n  ' + '\n  '.join(lines) + '\n'

        main_str += ')'
        return main_str

    def __dir__(self):
        module_attrs = dir(self._model.__class__)
        optimizer_attrs = dir(self.optimizer.__class__)
        attrs = list(self.__dict__.keys())
        losses = list(self._losses.keys())
        metrics = list(self._metrics.keys())
        regs = list(self._regs.keys())

        constraints = list(self._constraints.keys())
        keys = module_attrs + optimizer_attrs + attrs + losses + metrics + regs + constraints
        # Eliminate attrs that are not legal Python variable names
        keys = [key for key in keys if not key[0].isdigit()]

        return sorted(keys)

    def cpu(self):
        if isinstance(self._model, (nn.Module, Layer)):
            self._model.to("cpu")

    def cuda(self):
        if isinstance(self._model, (nn.Module, Layer)):
            self._model.to("cuda")

    @property
    def enable_tensorboard(self):
        return self._enable_tensorboard

    @enable_tensorboard.setter
    def enable_tensorboard(self, value):
        self._enable_tensorboard = value
        if value == True:
            if get_backend() == 'pytorch':
                try:
                    from trident.loggers.pytorch_tensorboard import SummaryWriter
                    self.training_context['summary_writer'] = SummaryWriter(os.path.join(working_directory, 'Logs'))

                except Exception as e:
                    print('Tensorboard initialize failed, please check the installation status about Tensorboard.')
                    print(e)
                    PrintException()
            elif get_backend() == 'tensorflow':
                try:
                    from trident.loggers.tensorflow_tensorboard import SummaryWriter
                    self.training_context['summary_writer'] = SummaryWriter(os.path.join(working_directory, 'Logs'))
                except Exception as e:
                    print('Tensorboard initialize failed, please check the installation status about Tensorboard.')
                    print(e)
                    PrintException()


class MuiltiNetwork(Model):
    def __init__(self, name=None):
        super().__init__(name=name)
        self._networks = OrderedDict()

    def add_network(self, name, inputs=None, input_shape=None, output=None, initializer=None):
        if output is not None:
            output.name = name
            if isinstance(output.input_shape, TensorShape):
                input_shape = output.input_shape
            if isinstance(output, Model):
                self._networks[name] = output
            else:
                self._networks[name] = Model(inputs=inputs, input_shape=input_shape, output=output)

    def __getattr__(self, name):
        if name in self.__dict__['_networks']:
            return self.__dict__['_networks'][name]
        elif name in ['steps', 'current_epoch', 'current_batch', 'frame_steps', 'train_steps']:
            if name not in self.__dict__['training_context']:
                self.__dict__['training_context'][name] = -1
            return self.__dict__['training_context'][name]
        elif name in ['_input_shape', '_output_shape', '_class_names', 'class_names', 'output_fn']:
            return self.__dict__[name]

        elif name in ['reverse_preprocess_flow']:
            return self.__getattribute__(name)

        if name == 'signature' or name == '_signature':
            _model = self.__dict__['_model']
            if _model is not None and isinstance(_model, Layer):
                return _model.signature
            else:
                return Signature()
        if 'training_context' in self.__dict__:
            if name in self.__dict__['training_context']:
                return self.__dict__['training_context'][name]
        if '_model' in self.__dict__:
            _model = self.__dict__['_model']

            if _model is not None and name in _model.__dict__['_parameters']:
                return _model.__dict__['_parameters'][name]
            elif _model is not None and name in _model.__dict__['_buffers']:
                return _model.__dict__['_buffers'][name]
            elif _model is not None and name in _model.__dict__['_modules']:
                return _model.__dict__['_modules'][name]
            elif _model is not None and name in _model.__dict__:
                return _model.__dict__[name]
            elif _model is not None and "_" + name in _model.__dict__:
                return _model.__dict__["_" + name]

        if name in self.__dict__:
            return self.__dict__[name]

        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, name))

    def __setattr__(self, name, value):
        if name in ['_networks']:
            object.__setattr__(self, '_networks', value)
        elif name in ['steps', 'current_epoch', 'current_batch', 'frame_steps', 'train_steps']:
            self.__dict__['training_context'][name] = value
            for k, v in self.__dict__['_networks'].items():
                v.training_context[name] = value
        elif name in ['_input_shape', '_output_shape', '_class_names', 'class_names', 'output_fn']:
            object.__setattr__(self, name, value)

        elif name in ['_model']:
            object.__setattr__(self, '_model', value)


        else:

            if name == 'signature' or name == '_signature':
                _model = self.__dict__['_model']
                if _model is not None and isinstance(_model, Layer):
                    object.__setattr__(_model, "_" + 'signature', value)
            if 'training_context' in self.__dict__ and name in self.__dict__['training_context']:
                self.__dict__['training_context'][name] = value
            elif '_model' in self.__dict__ and self.__dict__['_model']:
                _model = self.__dict__['_model']
                if _model is not None and name in _model.__dict__['_parameters']:
                    _model.__dict__['_parameters'][name] = value
                elif _model is not None and name in _model.__dict__['_buffers']:
                    _model.__dict__['_buffers'][name] = value
                elif _model is not None and name in _model.__dict__['_modules']:
                    _model.__dict__['_modules'][name] = value

                elif _model is not None and name in _model.__dict__:
                    object.__setattr__(self.__dict__['_model'], name, value)
                elif _model is not None and "_" + name in _model.__dict__:
                    object.__setattr__(self.__dict__['_model'], "_" + name, value)
                else:
                    object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)

    def with_optimizer(self, optimizer, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_optimizer(optimizer=optimizer, **kwargs)
        return self

    def with_loss(self, loss, loss_weight=1, start_epoch=0, name='', **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_loss(loss, loss_weight=loss_weight, start_epoch=start_epoch, name=name, **kwargs)

        return self

    def with_metric(self, metric, print_only=False, name='', **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_metric(metric, print_only=print_only, name=name, **kwargs)
        return self

    def with_regularizer(self, reg, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_regularizer(reg, **kwargs)
        return self

    def with_constraint(self, constraint, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_constraint(constraint, **kwargs)
        return self

    def with_initializer(self, initializer, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_initializer(initializer, **kwargs)
        return self

    def with_callbacks(self, *callbacks):
        for k in self._networks.keys():
            self._networks[k].with_callbacks(*callbacks)
        return self

    def with_model_save_path(self, save_path, **kwargs):
        for k in self._networks.keys():
            folder, filename, ext = split_path(save_path)
            current_save_path = os.path.join(folder, filename + '_' + k + ext)
            self._networks[k].with_model_save_path(current_save_path, **kwargs)
            self._networks[k].training_context['save_path'] = current_save_path
        return self

    def with_learning_rate_scheduler(self, lr_schedule, warmup=0, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_learning_rate_scheduler(lr_schedule, warmup, **kwargs)
        return self

    def with_automatic_mixed_precision_training(self, **kwargs):

        for k in self._networks.keys():
            self._networks[k].with_automatic_mixed_precision_training(**kwargs)
        return self

    def with_grad_clipping(self, clipping_threshold=3.0, **kwargs):
        for k in self._networks.keys():
            self._networks[k].with_grad_clipping(clipping_threshold, **kwargs)
        return self

    def adjust_learning_rate_scheduling(self, index: int, unit='batch', new_value: float = None):
        for k in self._networks.keys():
            self._networks[k].adjust_learning_rate_scheduling(index, unit, new_value)
        return self

    def adjust_learning_rate(self, lr):
        for k in self._networks.keys():
            self._networks[k].adjust_learning_rate(lr)
        return self

    def trigger_when(self, when='on_batch_end', frequency=None, unit='batch', action=None):
        new_callbacks = LambdaCallback(when, frequency=frequency, unit=unit, action=action)
        self.callbacks.append(new_callbacks)
        return self

    def unfreeze_model_scheduling(self, frequency: int, unit='epoch', slice_from=None, slice_to=None, module_name=None):
        for k in self._networks.keys():
            self._networks[k].unfreeze_model_scheduling(frequency, unit, slice_from, slice_to, module_name)
        return self

    def save_model(self, save_path=None, **kwargs):
        for k in self._networks.keys():
            self._networks[k].save_model(self._networks[k].training_context['save_path'], )
        return self

    def do_on_epoch_start(self):
        self.training_context['time_epoch_progress'] = 0
        self.training_context['time_batch_progress'] = 0
        for k in self._networks.keys():
            self._networks[k].do_on_epoch_start()

    def do_on_epoch_end(self):
        self.training_context['time_epoch_progress'] = 0

        total_loss = 0
        for k in self._networks.keys():
            self._networks[k].do_on_epoch_end()
            self.training_context['time_epoch_progress'] += self._networks[k].training_context['time_epoch_progress']
            steps, value = self._networks[k].epoch_loss_history.get_series('total_losses')
            for s, v in zip(steps, value):
                if s == self.training_context['current_epoch']:
                    total_loss += v
        self.epoch_loss_history.collect('total_losses', self.training_context['current_epoch'], total_loss)
        for callback in self.training_context['callbacks']:
            callback.on_epoch_end(self.training_context)

    def do_on_batch_start(self):
        if self.training_context['steps'] == 0:
            self.training_context['time_batch_progress'] = 0
        self.training_context['time_epoch_start'] = time.time()
        self.training_context['time_batch_start'] = time.time()
        # sub-model will do batch start automaticly
        # for k in self._networks.keys():
        #     # self._networks[k].do_on_batch_start()
        #     self._networks[k].training_context['time_epoch_start'] = time.time()
        #     self._networks[k].training_context['time_batch_start'] = time.time()

    def do_on_batch_end(self):
        self.training_context['time_batch_progress'] += (time.time() - self.training_context['time_batch_start'])
        self.training_context['time_epoch_progress'] += (time.time() - self.training_context['time_batch_start'])

    def do_post_gradient_update(self):
        pass

    def print_batch_progress(self, print_batch_progress_frequency):
        if 'max_name_length' not in self.training_context:
            self.training_context['max_name_length'] = len(self.name) + 1
        metric_strings = []
        slice_length = print_batch_progress_frequency // self.training_context['collect_data_inteval']
        for k in self.batch_metric_history.key_list:
            if k != 'epoch':
                metric_value = None
                batch_steps, batch_values = self.batch_metric_history.get_series(k)
                if len(batch_values) == 0:
                    batch_steps, batch_values = self.tmp_metrics.get_series(k)
                    metric_value = np.array(batch_values).mean()
                else:
                    if len(batch_values) > slice_length:
                        metric_value = np.array(batch_values[-1 * slice_length:]).mean()
                    else:
                        metric_value = np.array(batch_values).mean()

                metric_strings.append('{0}: {1} '.format(k, adaptive_format(metric_value, batch_values, value_type='metric', name=k)))

        loss_value = None
        loss_steps, loss_values = self.batch_loss_history.get_series('total_losses')
        if len(loss_values) == 0:
            loss_value = None
        else:
            if len(loss_values) > slice_length:
                loss_value = to_numpy(loss_values[-1 * slice_length:]).astype(np.float32).mean()
            else:
                loss_value = to_numpy(loss_values).astype(np.float32).mean()
        step_time = self.training_context['time_batch_progress']
        model.progress_bar(step_time, self.training_context['current_batch'], self.training_context['total_batch'] if self.training_context['total_batch'] is not None else '*',
                           'Loss: {0} | {1} | lr: {2:<10.3e} | epoch: {3}'.format(adaptive_format(loss_value, value_type='loss'), ', '.join(metric_strings),
                                                                                  self.training_context['current_lr'],
                                                                                  self.training_context['current_epoch']),
                           name=self.name.ljust(self.training_context['max_name_length'] + 1, ' '))
        self.training_context['time_batch_progress'] = 0

    def print_epoch_progress(self, *args, **kwargs):
        if 'max_name_length' not in self.training_context:
            self.training_context['max_name_length'] = len(self.name) + 1
        metric_strings = []
        for net in self._networks.value_list:
            for k in net.epoch_metric_history.key_list:
                if k != 'epoch':
                    metric_strings.append('{0}: {1}'.format(k, adaptive_format(net.epoch_metric_history.get_last(k)[-1], net.batch_metric_history.get_series(k)[-1], 'metric', k)))

        for k in self.epoch_metric_history.key_list:
            if k != 'epoch':
                metric_strings.append('{0}: {1}'.format(k, adaptive_format(self.epoch_metric_history.get_last(k)[-1], None, 'metric', k)))

        step_time = self.training_context['time_epoch_progress']
        total_losses = 0
        if 'total_losses' in self.epoch_loss_history:
            total_losses = self.epoch_loss_history['total_losses'][-1][-1]
        model.progress_bar(step_time, self.training_context['current_epoch'] + 1, self.training_context['total_epoch'],
                           'Loss: {0}| {1} | lr: {2:<10.3e}'.format(adaptive_format(total_losses, value_type='loss'), ', '.join(metric_strings),
                                                                    self._networks.value_list[0].training_context['current_lr']),
                           name=self.name.ljust(self.training_context['max_name_length'] + 1, ' '))
        self.training_context['time_epoch_progress'] = 0


class ImageClassificationModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(ImageClassificationModel, self).__init__(inputs, input_shape, output)

        self._class_names = []
        self._idx2lab = {}
        self._lab2idx = {}

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
        if self._model.signature is not None and len(self._model.signature.outputs.value_list) > 0 and self._model.signature.outputs.value_list[0].object_type is None:
            self._model.signature.outputs.value_list[0].object_type = ObjectType.classification_label

    @property
    def class_names(self):
        return self._class_names

    @class_names.setter
    def class_names(self, value):
        if self._class_names is not None and self._class_names != value:
            self._class_names = value
            self._lab2idx = {v: k for k, v in enumerate(self._class_names)}
            self._idx2lab = {k: v for k, v in enumerate(self._class_names)}

    def index2label(self, idx: int):
        if self._idx2lab is None or len(self._idx2lab.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif idx not in self._idx2lab:
            raise ValueError('Index :{0} is not exist in class names'.format(idx))
        else:
            return self._idx2lab[idx]

    def label2index(self, label):
        if self._lab2idx is None or len(self._lab2idx.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif label not in self._lab2idx:
            raise ValueError('label :{0} is not exist in class names'.format(label))
        else:
            return self._lab2idx[label]

    def infer_single_image(self, img, topk=1):
        if isinstance(self._model, Layer) and self._model.built:
            self._model.eval()
            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
            img = image_backend_adaption(img)
            inp = to_tensor(np.expand_dims(img, 0)).to(
                torch.device("cuda" if self._model.weights[0].data.is_cuda else "cpu")).to(
                self._model.weights[0].data.dtype)
            result = self._model(inp)
            result = to_numpy(result)[0]
            if self.class_names is None or len(self.class_names) == 0:
                return result
            else:
                # argresult = np.argsort(result)
                # argresult1 =argresult[::-1]
                answer = OrderedDict()
                idxs = list(np.argsort(result)[::-1][:topk])
                for idx in idxs:
                    prob = result[idx]
                    answer[self.index2label(idx)] = (idx, prob)
                # idx=int(np.argmax(result,-1)[0])

                return answer
        else:
            raise ValueError('the model is not built yet.')


class ImageRegressionModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(ImageRegressionModel, self).__init__(inputs, input_shape, output)
        if self._model._signature.inputs[self._model._signature.inputs.key_list[0]].object_type is None:
            self._model._signature.inputs[self._model._signature.inputs.key_list[0]].object_type = ObjectType.rgb
        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb

    def infer_single_image(self, img):
        if self._model.built:
            self._model.eval()
            img = image2array(img)
            img_shp = img.shape

            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            rescale_scale = 1.0
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
                    if (inspect.isfunction(func) and func.__qualname__ == 'resize.<locals>.img_op') or (isinstance(func, Transform) and func.name == 'resize'):
                        rescale_scale = func.scale
            img = image_backend_adaption(img)
            if isinstance(self._model, Layer):
                inp = to_tensor(np.expand_dims(img, 0)).to(self._model.device).to(self._model.weights[0].data.dtype)
                result = self._model(inp)
                result = to_numpy(result)
                return result.astype(np.int32)
            else:

                raise ValueError('the model is not layer.')


class ImageDetectionModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None, detection_threshold=0.5, nms_threshold=0.3):
        super(ImageDetectionModel, self).__init__(inputs, input_shape, output)

        object.__setattr__(self, 'detection_threshold', detection_threshold)
        object.__setattr__(self, 'nms_threshold', nms_threshold)

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb

    def infer_single_image(self, img, scale=1):
        if self._model.built:
            self._model.to(self.device)
            self._model.eval()

            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            rescale_scale = 1
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
                    if (inspect.isfunction(func) and func.__qualname__ == 'resize.<locals>.img_op') or (isinstance(func, Transform) and func.name == 'resize'):
                        rescale_scale = func.scale
            img = image_backend_adaption(img)
            inp = to_tensor(np.expand_dims(img, 0)).to(
                torch.device("cuda" if self._model.weights[0].data.is_cuda else "cpu")).to(
                self._model.weights[0].data.dtype)
            result = self._model(inp)

            bboxes = self.generate_bboxes(*result, threshold=self.detection_threshold, scale=scale)
            bboxes = self.nms(bboxes)
            # idx=int(np.argmax(result,-1)[0])
            return bboxes
        else:
            raise ValueError('the model is not built yet.')

    def generate_bboxes(self, *outputs, threshold=0.5, scale=1):
        raise NotImplementedError

    def nms(self, bboxes):
        raise NotImplementedError


class ImageSegmentationModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(ImageSegmentationModel, self).__init__(inputs, input_shape, output)

        self.palette = OrderedDict()
        self._class_names = []
        self._idx2lab = {}
        self._lab2idx = {}

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb

    @property
    def class_names(self):
        return self._class_names

    @class_names.setter
    def class_names(self, value):
        if self._class_names is not None and self._class_names != value:
            self._class_names = value
            self._lab2idx = {v: k for k, v in enumerate(self._class_names)}
            self._idx2lab = {k: v for k, v in enumerate(self._class_names)}

    def index2label(self, idx: int):
        if self._idx2lab is None or len(self._idx2lab.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif idx not in self._idx2lab:
            raise ValueError('Index :{0} is not exist in class names'.format(idx))
        else:
            return self._idx2lab[idx]

    def label2index(self, label):
        if self._lab2idx is None or len(self._lab2idx.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif label not in self._lab2idx:
            raise ValueError('label :{0} is not exist in class names'.format(label))
        else:
            return self._lab2idx[label]

    def infer_single_image(self, img):
        if isinstance(self._model, Layer) and self._model.built:
            self._model.eval()

            img = image2array(img)

            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
            img = image_backend_adaption(img)
            inp = to_tensor(np.expand_dims(img, 0)).to(
                torch.device("cuda" if self._model.weights[0].data.is_cuda else "cpu")).to(
                self._model.weights[0].data.dtype)
            result = argmax(self._model(inp)[0], axis=1)
            result = to_numpy(result)
            if self.class_names is None or len(self.class_names) == 0:
                return result
            else:
                if len(self.palette) > 0:
                    color_result = color2label(result, self.palette)
                    return color_result
                else:
                    return result
        else:
            raise ValueError('the model is not built yet.')


class ImageGenerationModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(ImageGenerationModel, self).__init__(inputs, input_shape, output)

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
        if self._model.signature is not None and len(self._model.signature.outputs.value_list) > 0 and self._model.signature.outputs.value_list[0].object_type is None:
            self._model.signature.outputs.value_list[0].object_type = ObjectType.rgb

    def infer_single_image(self, img):
        if self._model.built:
            self._model.eval()
            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            rescale_scale = 1.0
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
                    if (inspect.isfunction(func) and func.__qualname__ == 'resize.<locals>.img_op') or (isinstance(func, Transform) and func.name == 'resize'):
                        rescale_scale = func.scale
            img = image_backend_adaption(img)
            inp = to_tensor(np.expand_dims(img, 0)).to(torch.device("cuda" if self._model.weights[0].data.is_cuda else "cpu")).to(self._model.weights[0].data.dtype)
            result = self._model(inp)
            result = to_numpy(result)[0]

            for func in self.reverse_preprocess_flow:
                result = func(result)
            result = array2image(result)
            return result


class FaceLandmarkModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(FaceLandmarkModel, self).__init__(inputs, input_shape, output)

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
        if self._model.signature is not None and len(self._model.signature.outputs.value_list) > 0 and self._model.signature.outputs.value_list[0].object_type is None:
            self._model.signature.outputs.value_list[0].object_type = ObjectType.landmarks

    def infer_single_image(self, img):
        if self._model.built:
            self._model.eval()

            img = image2array(img)
            img_shp = img.shape

            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            rescale_scale = 1.0
            img_shape = int_shape(img)
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
                    if (inspect.isfunction(func) and func.__qualname__ == 'resize.<locals>.img_op') or (isinstance(func, Transform) and func.name == 'resize'):
                        rescale_scale = func.scale
            img = image_backend_adaption(img)
            if isinstance(self._model, Layer):
                inp = to_tensor(np.expand_dims(img, 0)).to(self._model.device).to(self._model.weights[0].data.dtype)
                result = self._model(inp)
                result = to_numpy(result) / rescale_scale
                result[:, :, 0::2] = clip(result[:, :, 0::2], 0, img_shp[1])
                result[:, :, 1::2] = clip(result[:, :, 1::2], 0, img_shp[0])
                return result  # .astype(np.int32)
            else:

                raise ValueError('the model is not layer.')

        else:
            raise ValueError('the model is not built yet.')


class FaceRecognitionModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(FaceRecognitionModel, self).__init__(inputs, input_shape, output)

        if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
            self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
        if self._model.signature is not None and len(self._model.signature.outputs.value_list) > 0 and self._model.signature.outputs.value_list[0].object_type is None:
            self._model.signature.outputs.value_list[0].object_type = ObjectType.embedding

    def infer_single_image(self, img):

        if isinstance(self._model, Layer) and self._model.built:
            self._model.eval()

            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]
            if self._model.signature is not None and len(self._model.signature.inputs.value_list) > 0 and self._model.signature.inputs.value_list[0].object_type is None:
                self._model.signature.inputs.value_list[0].object_type = ObjectType.rgb
            rescale_scale = 1.0
            for func in self.preprocess_flow:
                if (inspect.isfunction(func) or isinstance(func, Transform)) and func is not image_backend_adaption:
                    img = func(img, spec=self._model.input_spec)
                    if (inspect.isfunction(func) and func.__qualname__ == 'resize.<locals>.img_op') or (isinstance(func, Transform) and func.name == 'resize'):
                        rescale_scale = func.scale
            img = image_backend_adaption(img)
            inp = to_tensor(np.expand_dims(img, 0)).to(torch.device("cuda" if self._model.weights[0].data.is_cuda else "cpu")).to(self._model.weights[0].data.dtype)
            result = self._model(inp)[0]
            embedding = to_numpy(result)
            return embedding

        else:
            raise ValueError('the model is not built yet.')


class LanguageModel(Model):
    def __init__(self, inputs=None, input_shape=None, output=None):
        super(LanguageModel, self).__init__(inputs, input_shape, output)
        self.vocabs = None
        self.preprocess_flow = []

    def save_model(self, save_path=None, **kwargs):
        for callback in self.training_context['callbacks']:
            callback.on_model_saving_start(self.training_context)

        if isinstance(self._model, Layer) and any_abnormal_number(self._model):
            for para in self._model.parameters():
                if any_abnormal_number(para):
                    para.data.copy_(where(is_nan(para), random_normal_like(para, mean=0, std=0.02).to(get_device()), para))

            sys.stderr.write(self._get_name() + '  nan detected!!\n')
        if save_path is not None:
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filename = self.name
            self.training_context['save_path'] = save_path
        else:
            save_path = self.training_context['save_path']

        if isinstance(self._model, nn.Module):
            try:
                folder, filename, ext = split_path(save_path)
                if filename == '':
                    filename = self.name

                ext = '.pth.tar_'
                save_path = os.path.join(folder, filename + ext)
                make_dir_if_need(sanitize_path(save_path))
                save_path = sanitize_path(save_path)
                device = get_device()
                self._model.eval()
                self._model.cpu()
                torch.save({
                    'state_dict': self._model.state_dict(),
                    'vocabs': self.vocabs,
                    'backend': 'pytorch',
                    'trident_version': __version__,
                    'pytorch_version': torch.__version__,
                    'signature': self._model.signature
                }, save_path)

                shutil.copy2(save_path, save_path.replace('.pth.tar_', '.pth.tar'))
                os.remove(save_path)
                save_path = save_path.replace('pth.tar_', 'pth_')
                save(self._model, save_path)
                shutil.copy2(save_path, save_path.replace('.pth_', '.pth'))
                os.remove(save_path)
                self._model.train()
                self._model.to(device)
            except Exception as e:
                print(e)
                PrintException()

        elif isinstance(self._model, torch.Tensor):
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filenam = self.name

            ext = '.npy_'
            save_path = os.path.join(folder, filename + ext)
            make_dir_if_need(sanitize_path(save_path))
            save_path = sanitize_path(save_path)
            numpy_model = to_numpy(self._model)
            np.save(save_path, numpy_model)
            shutil.copy2(save_path, save_path.replace('.npy_', '.npy'))
            os.remove(save_path)
            sys.stdout.write('Yor model is a Tensor not a nn.Module, it has saved as numpy array(*.npy) successfully. ')
        else:
            raise ValueError('only Layer or nn.Module as model can export to onnx, yours model is {0}'.format(type(self._model)))

        for callback in self.training_context['callbacks']:
            callback.on_model_saving_end(self.training_context)

    def save_onnx(self, save_path, dynamic_axes=None, **kwargs):
        if isinstance(self._model, nn.Module):

            import_or_install('torch.onnx')
            self._model.eval()

            dummy_input = (to_tensor(self.signature.inputs.value_list[0].shape.get_dummy_tensor()))
            folder, filename, ext = split_path(save_path)
            if filename == '':
                filenam = self.name

            ext = '.onnx_'
            save_path = os.path.join(folder, filename + ext)
            make_dir_if_need(sanitize_path(save_path))
            save_path = sanitize_path(save_path)

            outputs = self._model(dummy_input)
            if dynamic_axes is None:
                dynamic_axes = {self.inputs.key_list[0]: [0],  # variable lenght axes
                                self.outputs.key_list[0]: [0]}

            # dynamic_axes = {}
            #
            # for inp in self.inputs.key_list:
            #     dynamic_axes[inp] = [0]
            # for out in self.outputs.key_list:
            #     dynamic_axes[out] = [0]
            torch.onnx.export(self._model,  # model being run
                              dummy_input,  # model input (or a tuple for multiple inputs)
                              save_path,  # where to save the model (can be a file or file-like object)
                              export_params=True,  # store the trained parameter weights inside the model file
                              opset_version=11,  # the ONNX version to export the model to
                              do_constant_folding=False,  # whether to execute constant folding for optimization
                              input_names=self.signature.inputs.key_list,  # the model's input names
                              output_names=self.signature.outputs.key_list,  # the model's output names
                              dynamic_axes=dynamic_axes)
            self._model.train()
            shutil.copy(save_path, save_path.replace('.onnx_', '.onnx'))
            os.remove(save_path)
            for callback in self.training_context['callbacks']:
                callback.on_model_saving_end(self.training_context)
        else:
            raise ValueError('only Layer or nn.Module as model can export to onnx, yours model is {0}'.format(type(self._model)))

    def load_model(self, file_path, **kwargs):
        print('Loading pretrained model from {}'.format(file_path))
        folder, filename, ext = split_path(file_path)
        if filename == '':
            filename = self.name
        state_dict = None
        pretrained_dict = None
        if ext == '.pth.tar':
            state_dict = torch.load(file_path, map_location=torch.device(get_device()))
        elif ext == '.pth':
            load_path = file_path
            if not os.path.exists(file_path):
                if os.path.exists(file_path.replace(ext, '.pth.tar')):
                    load_path = file_path.replace(ext, '.pth.tar')
                elif os.path.exists(os.path.join(working_directory, filename + ext)):
                    load_path = os.path.join(working_directory, filename + ext)
            recovery_pth = torch.load(load_path, map_location=torch.device(get_device()))

            if isinstance(recovery_pth, dict):
                state_dict = recovery_pth

            elif isinstance(recovery_pth, Layer):
                state_dict = recovery_pth.state_dict()

        if 'vocabs' in state_dict:
            self.vocabs = state_dict['vocabs']
        if 'backend' in state_dict and state_dict['backend'] != 'pytorch':
            raise RuntimeError(
                'The model archive {0} is a {1}-based model, but current backend is PyTorch, so cannot load model properly.'.format(file_path, state_dict['backend']))

        if "state_dict" in state_dict.keys():
            pretrained_dict = state_dict['state_dict']
        else:
            pretrained_dict = state_dict

        if isinstance(self._model, Layer):
            if check_keys(self._model, pretrained_dict):
                has_abnormal = False
                for key in pretrained_dict.keys():
                    value = pretrained_dict[key]
                    if is_tensor(value) and any_abnormal_number(value):
                        has_abnormal = True
                        print('detect abnormal in state_dict[{0}],value:{1}'.format(key), value)
                        pretrained_dict[key] = where(is_nan(value), random_normal_like(value, mean=0, std=0.02).to(get_device()).cast(value.dtype), value)
                    if is_tensor(value) and ndim(value) == 0:
                        pretrained_dict[key] = to_tensor(value.item())

                if has_abnormal:
                    sys.stderr.write(self._model._name + '  has_abnormal detected and  fixed!!\n')
                self._model.load_state_dict(pretrained_dict, strict=False)
                print('Model loaded!')
                # must switch to evluate first beforeinference or training
                # Dropout and Batch normalization will behavior change!!!

                self._model.eval()
        if "signature" in state_dict.keys() and (self._model.signature is None or state_dict['signature'] != self._model.signature):
            self._model.signature = state_dict['signature']
        self._model.to(get_device())
