# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: keras/protobuf/versions.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='keras/protobuf/versions.proto',
  package='third_party.py.keras.protobuf',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dkeras/protobuf/versions.proto\x12\x1dthird_party.py.keras.protobuf\"K\n\nVersionDef\x12\x10\n\x08producer\x18\x01 \x01(\x05\x12\x14\n\x0cmin_consumer\x18\x02 \x01(\x05\x12\x15\n\rbad_consumers\x18\x03 \x03(\x05\x62\x06proto3'
)




_VERSIONDEF = _descriptor.Descriptor(
  name='VersionDef',
  full_name='third_party.py.keras.protobuf.VersionDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='producer', full_name='third_party.py.keras.protobuf.VersionDef.producer', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_consumer', full_name='third_party.py.keras.protobuf.VersionDef.min_consumer', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bad_consumers', full_name='third_party.py.keras.protobuf.VersionDef.bad_consumers', index=2,
      number=3, type=5, cpp_type=1, label=3,
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
  serialized_start=64,
  serialized_end=139,
)

DESCRIPTOR.message_types_by_name['VersionDef'] = _VERSIONDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VersionDef = _reflection.GeneratedProtocolMessageType('VersionDef', (_message.Message,), {
  'DESCRIPTOR' : _VERSIONDEF,
  '__module__' : 'keras.protobuf.versions_pb2'
  # @@protoc_insertion_point(class_scope:third_party.py.keras.protobuf.VersionDef)
  })
_sym_db.RegisterMessage(VersionDef)


# @@protoc_insertion_point(module_scope)
