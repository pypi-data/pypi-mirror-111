# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import model_pb2 as model__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='service.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rservice.proto\x1a\x0bmodel.proto\"/\n\x11LoadModelsRequest\x12\x1a\n\x06models\x18\x01 \x03(\x0b\x32\n.ModelSpec\"%\n\x12LoadModelsResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x15\n\x13LoadedModelsRequest\"2\n\x14LoadedModelsResponse\x12\x1a\n\x06models\x18\x01 \x03(\x0b\x32\n.ModelSpec\"/\n\x12ModelStatusRequest\x12\x19\n\x05model\x18\x01 \x01(\x0b\x32\n.ModelSpec\"3\n\x13ModelStatusResponse\x12\x1c\n\x06status\x18\x01 \x01(\x0b\x32\x0c.ModelStatus\"\x15\n\x13ReloadModelsRequest\"\'\n\x14ReloadModelsResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\">\n\x0ePredictRequest\x12\x12\n\nmodel_name\x18\x01 \x01(\t\x12\r\n\x05\x62\x61tch\x18\x02 \x03(\t\x12\t\n\x01k\x18\x03 \x01(\x05\"N\n\x0fPredictResponse\x12 \n\x0bpredictions\x18\x01 \x03(\x0b\x32\x0b.Prediction\x12\x19\n\x05model\x18\x02 \x01(\x0b\x32\n.ModelSpec\"3\n\x0eVectorsRequest\x12\x12\n\nmodel_name\x18\x01 \x01(\t\x12\r\n\x05\x62\x61tch\x18\x02 \x03(\t\"J\n\x0fVectorsResponse\x12\x1c\n\x07vectors\x18\x01 \x03(\x0b\x32\x0b.WordVector\x12\x19\n\x05model\x18\x02 \x01(\x0b\x32\n.ModelSpec2\xe5\x02\n\x08\x46\x61stText\x12\x35\n\nLoadModels\x12\x12.LoadModelsRequest\x1a\x13.LoadModelsResponse\x12>\n\x0fGetLoadedModels\x12\x14.LoadedModelsRequest\x1a\x15.LoadedModelsResponse\x12;\n\x0eGetModelStatus\x12\x13.ModelStatusRequest\x1a\x14.ModelStatusResponse\x12\x41\n\x12ReloadConfigModels\x12\x14.ReloadModelsRequest\x1a\x15.ReloadModelsResponse\x12,\n\x07Predict\x12\x0f.PredictRequest\x1a\x10.PredictResponse\x12\x34\n\x0fGetWordsVectors\x12\x0f.VectorsRequest\x1a\x10.VectorsResponseb\x06proto3'
  ,
  dependencies=[model__pb2.DESCRIPTOR,])




_LOADMODELSREQUEST = _descriptor.Descriptor(
  name='LoadModelsRequest',
  full_name='LoadModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='LoadModelsRequest.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=77,
)


_LOADMODELSRESPONSE = _descriptor.Descriptor(
  name='LoadModelsResponse',
  full_name='LoadModelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='LoadModelsResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=116,
)


_LOADEDMODELSREQUEST = _descriptor.Descriptor(
  name='LoadedModelsRequest',
  full_name='LoadedModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=118,
  serialized_end=139,
)


_LOADEDMODELSRESPONSE = _descriptor.Descriptor(
  name='LoadedModelsResponse',
  full_name='LoadedModelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='LoadedModelsResponse.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=141,
  serialized_end=191,
)


_MODELSTATUSREQUEST = _descriptor.Descriptor(
  name='ModelStatusRequest',
  full_name='ModelStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='ModelStatusRequest.model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=193,
  serialized_end=240,
)


_MODELSTATUSRESPONSE = _descriptor.Descriptor(
  name='ModelStatusResponse',
  full_name='ModelStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ModelStatusResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=293,
)


_RELOADMODELSREQUEST = _descriptor.Descriptor(
  name='ReloadModelsRequest',
  full_name='ReloadModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=295,
  serialized_end=316,
)


_RELOADMODELSRESPONSE = _descriptor.Descriptor(
  name='ReloadModelsResponse',
  full_name='ReloadModelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='ReloadModelsResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=318,
  serialized_end=357,
)


_PREDICTREQUEST = _descriptor.Descriptor(
  name='PredictRequest',
  full_name='PredictRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_name', full_name='PredictRequest.model_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch', full_name='PredictRequest.batch', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='k', full_name='PredictRequest.k', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=421,
)


_PREDICTRESPONSE = _descriptor.Descriptor(
  name='PredictResponse',
  full_name='PredictResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='predictions', full_name='PredictResponse.predictions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model', full_name='PredictResponse.model', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=423,
  serialized_end=501,
)


_VECTORSREQUEST = _descriptor.Descriptor(
  name='VectorsRequest',
  full_name='VectorsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_name', full_name='VectorsRequest.model_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch', full_name='VectorsRequest.batch', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=503,
  serialized_end=554,
)


_VECTORSRESPONSE = _descriptor.Descriptor(
  name='VectorsResponse',
  full_name='VectorsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='vectors', full_name='VectorsResponse.vectors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model', full_name='VectorsResponse.model', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=556,
  serialized_end=630,
)

_LOADMODELSREQUEST.fields_by_name['models'].message_type = model__pb2._MODELSPEC
_LOADEDMODELSRESPONSE.fields_by_name['models'].message_type = model__pb2._MODELSPEC
_MODELSTATUSREQUEST.fields_by_name['model'].message_type = model__pb2._MODELSPEC
_MODELSTATUSRESPONSE.fields_by_name['status'].message_type = model__pb2._MODELSTATUS
_PREDICTRESPONSE.fields_by_name['predictions'].message_type = model__pb2._PREDICTION
_PREDICTRESPONSE.fields_by_name['model'].message_type = model__pb2._MODELSPEC
_VECTORSRESPONSE.fields_by_name['vectors'].message_type = model__pb2._WORDVECTOR
_VECTORSRESPONSE.fields_by_name['model'].message_type = model__pb2._MODELSPEC
DESCRIPTOR.message_types_by_name['LoadModelsRequest'] = _LOADMODELSREQUEST
DESCRIPTOR.message_types_by_name['LoadModelsResponse'] = _LOADMODELSRESPONSE
DESCRIPTOR.message_types_by_name['LoadedModelsRequest'] = _LOADEDMODELSREQUEST
DESCRIPTOR.message_types_by_name['LoadedModelsResponse'] = _LOADEDMODELSRESPONSE
DESCRIPTOR.message_types_by_name['ModelStatusRequest'] = _MODELSTATUSREQUEST
DESCRIPTOR.message_types_by_name['ModelStatusResponse'] = _MODELSTATUSRESPONSE
DESCRIPTOR.message_types_by_name['ReloadModelsRequest'] = _RELOADMODELSREQUEST
DESCRIPTOR.message_types_by_name['ReloadModelsResponse'] = _RELOADMODELSRESPONSE
DESCRIPTOR.message_types_by_name['PredictRequest'] = _PREDICTREQUEST
DESCRIPTOR.message_types_by_name['PredictResponse'] = _PREDICTRESPONSE
DESCRIPTOR.message_types_by_name['VectorsRequest'] = _VECTORSREQUEST
DESCRIPTOR.message_types_by_name['VectorsResponse'] = _VECTORSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LoadModelsRequest = _reflection.GeneratedProtocolMessageType('LoadModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOADMODELSREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:LoadModelsRequest)
  })
_sym_db.RegisterMessage(LoadModelsRequest)

LoadModelsResponse = _reflection.GeneratedProtocolMessageType('LoadModelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOADMODELSRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:LoadModelsResponse)
  })
_sym_db.RegisterMessage(LoadModelsResponse)

LoadedModelsRequest = _reflection.GeneratedProtocolMessageType('LoadedModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOADEDMODELSREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:LoadedModelsRequest)
  })
_sym_db.RegisterMessage(LoadedModelsRequest)

LoadedModelsResponse = _reflection.GeneratedProtocolMessageType('LoadedModelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOADEDMODELSRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:LoadedModelsResponse)
  })
_sym_db.RegisterMessage(LoadedModelsResponse)

ModelStatusRequest = _reflection.GeneratedProtocolMessageType('ModelStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _MODELSTATUSREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ModelStatusRequest)
  })
_sym_db.RegisterMessage(ModelStatusRequest)

ModelStatusResponse = _reflection.GeneratedProtocolMessageType('ModelStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _MODELSTATUSRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ModelStatusResponse)
  })
_sym_db.RegisterMessage(ModelStatusResponse)

ReloadModelsRequest = _reflection.GeneratedProtocolMessageType('ReloadModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _RELOADMODELSREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ReloadModelsRequest)
  })
_sym_db.RegisterMessage(ReloadModelsRequest)

ReloadModelsResponse = _reflection.GeneratedProtocolMessageType('ReloadModelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _RELOADMODELSRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ReloadModelsResponse)
  })
_sym_db.RegisterMessage(ReloadModelsResponse)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:PredictRequest)
  })
_sym_db.RegisterMessage(PredictRequest)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:PredictResponse)
  })
_sym_db.RegisterMessage(PredictResponse)

VectorsRequest = _reflection.GeneratedProtocolMessageType('VectorsRequest', (_message.Message,), {
  'DESCRIPTOR' : _VECTORSREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:VectorsRequest)
  })
_sym_db.RegisterMessage(VectorsRequest)

VectorsResponse = _reflection.GeneratedProtocolMessageType('VectorsResponse', (_message.Message,), {
  'DESCRIPTOR' : _VECTORSRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:VectorsResponse)
  })
_sym_db.RegisterMessage(VectorsResponse)



_FASTTEXT = _descriptor.ServiceDescriptor(
  name='FastText',
  full_name='FastText',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=633,
  serialized_end=990,
  methods=[
  _descriptor.MethodDescriptor(
    name='LoadModels',
    full_name='FastText.LoadModels',
    index=0,
    containing_service=None,
    input_type=_LOADMODELSREQUEST,
    output_type=_LOADMODELSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetLoadedModels',
    full_name='FastText.GetLoadedModels',
    index=1,
    containing_service=None,
    input_type=_LOADEDMODELSREQUEST,
    output_type=_LOADEDMODELSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetModelStatus',
    full_name='FastText.GetModelStatus',
    index=2,
    containing_service=None,
    input_type=_MODELSTATUSREQUEST,
    output_type=_MODELSTATUSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ReloadConfigModels',
    full_name='FastText.ReloadConfigModels',
    index=3,
    containing_service=None,
    input_type=_RELOADMODELSREQUEST,
    output_type=_RELOADMODELSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Predict',
    full_name='FastText.Predict',
    index=4,
    containing_service=None,
    input_type=_PREDICTREQUEST,
    output_type=_PREDICTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetWordsVectors',
    full_name='FastText.GetWordsVectors',
    index=5,
    containing_service=None,
    input_type=_VECTORSREQUEST,
    output_type=_VECTORSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FASTTEXT)

DESCRIPTOR.services_by_name['FastText'] = _FASTTEXT

# @@protoc_insertion_point(module_scope)
