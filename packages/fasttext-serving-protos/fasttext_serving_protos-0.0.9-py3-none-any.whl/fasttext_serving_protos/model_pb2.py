# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='model.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bmodel.proto\"=\n\tModelSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tbase_path\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x03\"\x88\x01\n\x0bModelStatus\x12&\n\x05state\x18\x01 \x01(\x0e\x32\x17.ModelStatus.ModelState\x12\x0f\n\x07version\x18\x02 \x01(\x03\"@\n\nModelState\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06LOADED\x10\x01\x12\r\n\tAVAILABLE\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\",\n\nPrediction\x12\x0e\n\x06labels\x18\x01 \x03(\t\x12\x0e\n\x06scores\x18\x02 \x03(\x02\"\x1d\n\nWordVector\x12\x0f\n\x07\x65lement\x18\x01 \x03(\x02\x62\x06proto3'
)



_MODELSTATUS_MODELSTATE = _descriptor.EnumDescriptor(
  name='ModelState',
  full_name='ModelStatus.ModelState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOADED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AVAILABLE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=151,
  serialized_end=215,
)
_sym_db.RegisterEnumDescriptor(_MODELSTATUS_MODELSTATE)


_MODELSPEC = _descriptor.Descriptor(
  name='ModelSpec',
  full_name='ModelSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ModelSpec.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_path', full_name='ModelSpec.base_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='ModelSpec.version', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=15,
  serialized_end=76,
)


_MODELSTATUS = _descriptor.Descriptor(
  name='ModelStatus',
  full_name='ModelStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='ModelStatus.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='ModelStatus.version', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MODELSTATUS_MODELSTATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=215,
)


_PREDICTION = _descriptor.Descriptor(
  name='Prediction',
  full_name='Prediction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='labels', full_name='Prediction.labels', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scores', full_name='Prediction.scores', index=1,
      number=2, type=2, cpp_type=6, label=3,
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
  serialized_start=217,
  serialized_end=261,
)


_WORDVECTOR = _descriptor.Descriptor(
  name='WordVector',
  full_name='WordVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='WordVector.element', index=0,
      number=1, type=2, cpp_type=6, label=3,
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
  serialized_start=263,
  serialized_end=292,
)

_MODELSTATUS.fields_by_name['state'].enum_type = _MODELSTATUS_MODELSTATE
_MODELSTATUS_MODELSTATE.containing_type = _MODELSTATUS
DESCRIPTOR.message_types_by_name['ModelSpec'] = _MODELSPEC
DESCRIPTOR.message_types_by_name['ModelStatus'] = _MODELSTATUS
DESCRIPTOR.message_types_by_name['Prediction'] = _PREDICTION
DESCRIPTOR.message_types_by_name['WordVector'] = _WORDVECTOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModelSpec = _reflection.GeneratedProtocolMessageType('ModelSpec', (_message.Message,), {
  'DESCRIPTOR' : _MODELSPEC,
  '__module__' : 'model_pb2'
  # @@protoc_insertion_point(class_scope:ModelSpec)
  })
_sym_db.RegisterMessage(ModelSpec)

ModelStatus = _reflection.GeneratedProtocolMessageType('ModelStatus', (_message.Message,), {
  'DESCRIPTOR' : _MODELSTATUS,
  '__module__' : 'model_pb2'
  # @@protoc_insertion_point(class_scope:ModelStatus)
  })
_sym_db.RegisterMessage(ModelStatus)

Prediction = _reflection.GeneratedProtocolMessageType('Prediction', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTION,
  '__module__' : 'model_pb2'
  # @@protoc_insertion_point(class_scope:Prediction)
  })
_sym_db.RegisterMessage(Prediction)

WordVector = _reflection.GeneratedProtocolMessageType('WordVector', (_message.Message,), {
  'DESCRIPTOR' : _WORDVECTOR,
  '__module__' : 'model_pb2'
  # @@protoc_insertion_point(class_scope:WordVector)
  })
_sym_db.RegisterMessage(WordVector)


# @@protoc_insertion_point(module_scope)
