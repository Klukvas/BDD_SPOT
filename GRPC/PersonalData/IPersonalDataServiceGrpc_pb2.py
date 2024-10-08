# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: IPersonalDataServiceGrpc.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from GRPC.UsefulImport import empty_pb2 as empty__pb2
from GRPC.UsefulImport import bcl_pb2 as bcl__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eIPersonalDataServiceGrpc.proto\x12\x19Service.PersonalData.Grpc\x1a\x0b\x65mpty.proto\x1a\tbcl.proto\"m\n\x14\x41uditLogGrpcContract\x12\x10\n\x08TraderId\x18\x01 \x01(\t\x12\n\n\x02Ip\x18\x02 \x01(\t\x12\x13\n\x0bServiceName\x18\x03 \x01(\t\x12\x11\n\tProcessId\x18\x04 \x01(\t\x12\x0f\n\x07\x43ontext\x18\x05 \x01(\t\"\x81\x01\n\x10\x43onfirmGrpcModel\x12\n\n\x02Id\x18\x01 \x01(\t\x12\x1e\n\x07\x43onfirm\x18\x02 \x01(\x0b\x32\r.bcl.DateTime\x12\x41\n\x08\x41uditLog\x18\x03 \x01(\x0b\x32/.Service.PersonalData.Grpc.AuditLogGrpcContract\"3\n\x15\x45xternalDataGrpcModel\x12\x0b\n\x03Key\x18\x01 \x01(\t\x12\r\n\x05Value\x18\x02 \x01(\t\"\"\n\x11GetByEmailRequest\x12\r\n\x05\x45mail\x18\x01 \x01(\t\"\x1c\n\x0eGetByIdRequest\x12\n\n\x02Id\x18\x01 \x01(\t\"\x1e\n\x0fGetByIdsRequest\x12\x0b\n\x03Ids\x18\x01 \x03(\t\"\"\n\x11GetByPhoneRequest\x12\r\n\x05Phone\x18\x01 \x01(\t\"`\n\x1eGetPersonalDataByStatusRequest\x12>\n\x06Status\x18\x01 \x01(\x0e\x32..Service.PersonalData.Grpc.PersonalDataKYCEnum\"o\n\x1fGetPersonalDataByStatusResponse\x12L\n\x12PersonalDataModels\x18\x01 \x03(\x0b\x32\x30.Service.PersonalData.Grpc.PersonalDataGrpcModel\"+\n\nGetRequest\x12\r\n\x05Limit\x18\x01 \x01(\x05\x12\x0e\n\x06Offset\x18\x02 \x01(\x05\".\n\x10GetTotalResponse\x12\x1a\n\x12TotalPersonalDatas\x18\x01 \x01(\x05\"l\n!PersonalDataBatchResponseContract\x12G\n\rPersonalDatas\x18\x01 \x03(\x0b\x32\x30.Service.PersonalData.Grpc.PersonalDataGrpcModel\"\xd6\x05\n\x15PersonalDataGrpcModel\x12\n\n\x02Id\x18\x01 \x01(\t\x12\r\n\x05\x45mail\x18\x02 \x01(\t\x12\x11\n\tFirstName\x18\x03 \x01(\t\x12\x10\n\x08LastName\x18\x04 \x01(\t\x12;\n\x03Sex\x18\x05 \x01(\x0e\x32..Service.PersonalData.Grpc.PersonalDataSexEnum\x12\"\n\x0b\x44\x61teOfBirth\x18\x06 \x01(\x0b\x32\r.bcl.DateTime\x12\x1a\n\x12\x43ountryOfResidence\x18\x07 \x01(\t\x12\x1c\n\x14\x43ountryOfCitizenship\x18\x08 \x01(\t\x12\x0c\n\x04\x43ity\x18\t \x01(\t\x12\x12\n\nPostalCode\x18\n \x01(\t\x12\r\n\x05Phone\x18\x0b \x01(\t\x12;\n\x03KYC\x18\x0c \x01(\x0e\x32..Service.PersonalData.Grpc.PersonalDataKYCEnum\x12\x1e\n\x07\x43onfirm\x18\r \x01(\x0b\x32\r.bcl.DateTime\x12\x41\n\x08\x41uditLog\x18\x0e \x01(\x0b\x32/.Service.PersonalData.Grpc.AuditLogGrpcContract\x12\x0f\n\x07\x41\x64\x64ress\x18\x0f \x01(\t\x12\x11\n\tUSCitizen\x18\x10 \x01(\x08\x12\x1d\n\x15\x43ountryOfRegistration\x18\x11 \x01(\t\x12\x18\n\x10IpOfRegistration\x18\x12 \x01(\t\x12\x46\n\x0c\x45xternalData\x18\x13 \x03(\x0b\x32\x30.Service.PersonalData.Grpc.ExternalDataGrpcModel\x12\x0f\n\x07\x42randId\x18\x14 \x01(\t\x12\x14\n\x0cPlatformType\x18\x15 \x01(\t\x12#\n\x0c\x43onfirmPhone\x18\x16 \x01(\x0b\x32\r.bcl.DateTime\x12 \n\tCreatedAt\x18\x17 \x01(\x0b\x32\r.bcl.DateTime\"j\n PersonalDataGrpcResponseContract\x12\x46\n\x0cPersonalData\x18\x01 \x01(\x0b\x32\x30.Service.PersonalData.Grpc.PersonalDataGrpcModel\"\xd2\x01\n\x1dRegisterPersonalDataGrpcModel\x12\n\n\x02Id\x18\x01 \x01(\t\x12\r\n\x05\x45mail\x18\x02 \x01(\t\x12\x1a\n\x12\x43ountryOfResidence\x18\x03 \x01(\t\x12\x1d\n\x15\x43ountryOfRegistration\x18\x04 \x01(\t\x12\x18\n\x10IpOfRegistration\x18\x05 \x01(\t\x12\x41\n\x08\x41uditLog\x18\x06 \x01(\x0b\x32/.Service.PersonalData.Grpc.AuditLogGrpcContract\" \n\x12ResultGrpcResponse\x12\n\n\x02Ok\x18\x01 \x01(\x08\"#\n\rSearchRequest\x12\x12\n\nSearchText\x18\x01 \x01(\t\"\xa3\x01\n\x15UpdateKycGrpcContract\x12\n\n\x02Id\x18\x01 \x01(\t\x12;\n\x03Kyc\x18\x02 \x01(\x0e\x32..Service.PersonalData.Grpc.PersonalDataKYCEnum\x12\x41\n\x08\x41uditLog\x18\x03 \x01(\x0b\x32/.Service.PersonalData.Grpc.AuditLogGrpcContract\"\x84\x03\n\x1eUpdatePersonalDataGrpcContract\x12\n\n\x02Id\x18\x01 \x01(\t\x12\x11\n\tFirstName\x18\x02 \x01(\t\x12\x10\n\x08LastName\x18\x03 \x01(\t\x12;\n\x03Sex\x18\x04 \x01(\x0e\x32..Service.PersonalData.Grpc.PersonalDataSexEnum\x12\"\n\x0b\x44\x61teOfBirth\x18\x05 \x01(\x0b\x32\r.bcl.DateTime\x12\x1a\n\x12\x43ountryOfResidence\x18\x06 \x01(\t\x12\x1c\n\x14\x43ountryOfCitizenship\x18\x07 \x01(\t\x12\x0c\n\x04\x43ity\x18\x08 \x01(\t\x12\x12\n\nPostalCode\x18\t \x01(\t\x12\r\n\x05Phone\x18\n \x01(\t\x12\x41\n\x08\x41uditLog\x18\x0b \x01(\x0b\x32/.Service.PersonalData.Grpc.AuditLogGrpcContract\x12\x0f\n\x07\x41\x64\x64ress\x18\x0c \x01(\t\x12\x11\n\tUSCitizen\x18\r \x01(\x08*X\n\x13PersonalDataKYCEnum\x12\x0f\n\x0bNotVerified\x10\x00\x12\x12\n\x0eOnVerification\x10\x01\x12\x0c\n\x08Verified\x10\x02\x12\x0e\n\nRestricted\x10\x03*8\n\x13PersonalDataSexEnum\x12\x0b\n\x07Unknown\x10\x00\x12\x08\n\x04Male\x10\x01\x12\n\n\x06\x46\x65male\x10\x02\x32\x9b\x0b\n\x17PersonalDataServiceGrpc\x12N\n\x07\x43onfirm\x12+.Service.PersonalData.Grpc.ConfirmGrpcModel\x1a\x16.google.protobuf.Empty\x12S\n\x0c\x43onfirmPhone\x12+.Service.PersonalData.Grpc.ConfirmGrpcModel\x1a\x16.google.protobuf.Empty\x12j\n\x03Get\x12%.Service.PersonalData.Grpc.GetRequest\x1a<.Service.PersonalData.Grpc.PersonalDataBatchResponseContract\x12w\n\nGetByEmail\x12,.Service.PersonalData.Grpc.GetByEmailRequest\x1a;.Service.PersonalData.Grpc.PersonalDataGrpcResponseContract\x12q\n\x07GetById\x12).Service.PersonalData.Grpc.GetByIdRequest\x1a;.Service.PersonalData.Grpc.PersonalDataGrpcResponseContract\x12t\n\x08GetByIds\x12*.Service.PersonalData.Grpc.GetByIdsRequest\x1a<.Service.PersonalData.Grpc.PersonalDataBatchResponseContract\x12w\n\nGetByPhone\x12,.Service.PersonalData.Grpc.GetByPhoneRequest\x1a;.Service.PersonalData.Grpc.PersonalDataGrpcResponseContract\x12\x90\x01\n\x17GetPersonalDataByStatus\x12\x39.Service.PersonalData.Grpc.GetPersonalDataByStatusRequest\x1a:.Service.PersonalData.Grpc.GetPersonalDataByStatusResponse\x12O\n\x08GetTotal\x12\x16.google.protobuf.Empty\x1a+.Service.PersonalData.Grpc.GetTotalResponse\x12s\n\x08Register\x12\x38.Service.PersonalData.Grpc.RegisterPersonalDataGrpcModel\x1a-.Service.PersonalData.Grpc.ResultGrpcResponse\x12p\n\x06Search\x12(.Service.PersonalData.Grpc.SearchRequest\x1a<.Service.PersonalData.Grpc.PersonalDataBatchResponseContract\x12r\n\x06Update\x12\x39.Service.PersonalData.Grpc.UpdatePersonalDataGrpcContract\x1a-.Service.PersonalData.Grpc.ResultGrpcResponse\x12U\n\tUpdateKyc\x12\x30.Service.PersonalData.Grpc.UpdateKycGrpcContract\x1a\x16.google.protobuf.Emptyb\x06proto3')

_PERSONALDATAKYCENUM = DESCRIPTOR.enum_types_by_name['PersonalDataKYCEnum']
PersonalDataKYCEnum = enum_type_wrapper.EnumTypeWrapper(_PERSONALDATAKYCENUM)
_PERSONALDATASEXENUM = DESCRIPTOR.enum_types_by_name['PersonalDataSexEnum']
PersonalDataSexEnum = enum_type_wrapper.EnumTypeWrapper(_PERSONALDATASEXENUM)
NotVerified = 0
OnVerification = 1
Verified = 2
Restricted = 3
Unknown = 0
Male = 1
Female = 2


_AUDITLOGGRPCCONTRACT = DESCRIPTOR.message_types_by_name['AuditLogGrpcContract']
_CONFIRMGRPCMODEL = DESCRIPTOR.message_types_by_name['ConfirmGrpcModel']
_EXTERNALDATAGRPCMODEL = DESCRIPTOR.message_types_by_name['ExternalDataGrpcModel']
_GETBYEMAILREQUEST = DESCRIPTOR.message_types_by_name['GetByEmailRequest']
_GETBYIDREQUEST = DESCRIPTOR.message_types_by_name['GetByIdRequest']
_GETBYIDSREQUEST = DESCRIPTOR.message_types_by_name['GetByIdsRequest']
_GETBYPHONEREQUEST = DESCRIPTOR.message_types_by_name['GetByPhoneRequest']
_GETPERSONALDATABYSTATUSREQUEST = DESCRIPTOR.message_types_by_name['GetPersonalDataByStatusRequest']
_GETPERSONALDATABYSTATUSRESPONSE = DESCRIPTOR.message_types_by_name['GetPersonalDataByStatusResponse']
_GETREQUEST = DESCRIPTOR.message_types_by_name['GetRequest']
_GETTOTALRESPONSE = DESCRIPTOR.message_types_by_name['GetTotalResponse']
_PERSONALDATABATCHRESPONSECONTRACT = DESCRIPTOR.message_types_by_name['PersonalDataBatchResponseContract']
_PERSONALDATAGRPCMODEL = DESCRIPTOR.message_types_by_name['PersonalDataGrpcModel']
_PERSONALDATAGRPCRESPONSECONTRACT = DESCRIPTOR.message_types_by_name['PersonalDataGrpcResponseContract']
_REGISTERPERSONALDATAGRPCMODEL = DESCRIPTOR.message_types_by_name['RegisterPersonalDataGrpcModel']
_RESULTGRPCRESPONSE = DESCRIPTOR.message_types_by_name['ResultGrpcResponse']
_SEARCHREQUEST = DESCRIPTOR.message_types_by_name['SearchRequest']
_UPDATEKYCGRPCCONTRACT = DESCRIPTOR.message_types_by_name['UpdateKycGrpcContract']
_UPDATEPERSONALDATAGRPCCONTRACT = DESCRIPTOR.message_types_by_name['UpdatePersonalDataGrpcContract']
AuditLogGrpcContract = _reflection.GeneratedProtocolMessageType('AuditLogGrpcContract', (_message.Message,), {
  'DESCRIPTOR' : _AUDITLOGGRPCCONTRACT,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.AuditLogGrpcContract)
  })
_sym_db.RegisterMessage(AuditLogGrpcContract)

ConfirmGrpcModel = _reflection.GeneratedProtocolMessageType('ConfirmGrpcModel', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMGRPCMODEL,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.ConfirmGrpcModel)
  })
_sym_db.RegisterMessage(ConfirmGrpcModel)

ExternalDataGrpcModel = _reflection.GeneratedProtocolMessageType('ExternalDataGrpcModel', (_message.Message,), {
  'DESCRIPTOR' : _EXTERNALDATAGRPCMODEL,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.ExternalDataGrpcModel)
  })
_sym_db.RegisterMessage(ExternalDataGrpcModel)

GetByEmailRequest = _reflection.GeneratedProtocolMessageType('GetByEmailRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBYEMAILREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetByEmailRequest)
  })
_sym_db.RegisterMessage(GetByEmailRequest)

GetByIdRequest = _reflection.GeneratedProtocolMessageType('GetByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBYIDREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetByIdRequest)
  })
_sym_db.RegisterMessage(GetByIdRequest)

GetByIdsRequest = _reflection.GeneratedProtocolMessageType('GetByIdsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBYIDSREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetByIdsRequest)
  })
_sym_db.RegisterMessage(GetByIdsRequest)

GetByPhoneRequest = _reflection.GeneratedProtocolMessageType('GetByPhoneRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBYPHONEREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetByPhoneRequest)
  })
_sym_db.RegisterMessage(GetByPhoneRequest)

GetPersonalDataByStatusRequest = _reflection.GeneratedProtocolMessageType('GetPersonalDataByStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPERSONALDATABYSTATUSREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetPersonalDataByStatusRequest)
  })
_sym_db.RegisterMessage(GetPersonalDataByStatusRequest)

GetPersonalDataByStatusResponse = _reflection.GeneratedProtocolMessageType('GetPersonalDataByStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPERSONALDATABYSTATUSRESPONSE,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetPersonalDataByStatusResponse)
  })
_sym_db.RegisterMessage(GetPersonalDataByStatusResponse)

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetRequest)
  })
_sym_db.RegisterMessage(GetRequest)

GetTotalResponse = _reflection.GeneratedProtocolMessageType('GetTotalResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTOTALRESPONSE,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.GetTotalResponse)
  })
_sym_db.RegisterMessage(GetTotalResponse)

PersonalDataBatchResponseContract = _reflection.GeneratedProtocolMessageType('PersonalDataBatchResponseContract', (_message.Message,), {
  'DESCRIPTOR' : _PERSONALDATABATCHRESPONSECONTRACT,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.PersonalDataBatchResponseContract)
  })
_sym_db.RegisterMessage(PersonalDataBatchResponseContract)

PersonalDataGrpcModel = _reflection.GeneratedProtocolMessageType('PersonalDataGrpcModel', (_message.Message,), {
  'DESCRIPTOR' : _PERSONALDATAGRPCMODEL,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.PersonalDataGrpcModel)
  })
_sym_db.RegisterMessage(PersonalDataGrpcModel)

PersonalDataGrpcResponseContract = _reflection.GeneratedProtocolMessageType('PersonalDataGrpcResponseContract', (_message.Message,), {
  'DESCRIPTOR' : _PERSONALDATAGRPCRESPONSECONTRACT,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.PersonalDataGrpcResponseContract)
  })
_sym_db.RegisterMessage(PersonalDataGrpcResponseContract)

RegisterPersonalDataGrpcModel = _reflection.GeneratedProtocolMessageType('RegisterPersonalDataGrpcModel', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERPERSONALDATAGRPCMODEL,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.RegisterPersonalDataGrpcModel)
  })
_sym_db.RegisterMessage(RegisterPersonalDataGrpcModel)

ResultGrpcResponse = _reflection.GeneratedProtocolMessageType('ResultGrpcResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESULTGRPCRESPONSE,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.ResultGrpcResponse)
  })
_sym_db.RegisterMessage(ResultGrpcResponse)

SearchRequest = _reflection.GeneratedProtocolMessageType('SearchRequest', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.SearchRequest)
  })
_sym_db.RegisterMessage(SearchRequest)

UpdateKycGrpcContract = _reflection.GeneratedProtocolMessageType('UpdateKycGrpcContract', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEKYCGRPCCONTRACT,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.UpdateKycGrpcContract)
  })
_sym_db.RegisterMessage(UpdateKycGrpcContract)

UpdatePersonalDataGrpcContract = _reflection.GeneratedProtocolMessageType('UpdatePersonalDataGrpcContract', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPERSONALDATAGRPCCONTRACT,
  '__module__' : 'IPersonalDataServiceGrpc_pb2'
  # @@protoc_insertion_point(class_scope:Service.PersonalData.Grpc.UpdatePersonalDataGrpcContract)
  })
_sym_db.RegisterMessage(UpdatePersonalDataGrpcContract)

_PERSONALDATASERVICEGRPC = DESCRIPTOR.services_by_name['PersonalDataServiceGrpc']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PERSONALDATAKYCENUM._serialized_start=2607
  _PERSONALDATAKYCENUM._serialized_end=2695
  _PERSONALDATASEXENUM._serialized_start=2697
  _PERSONALDATASEXENUM._serialized_end=2753
  _AUDITLOGGRPCCONTRACT._serialized_start=85
  _AUDITLOGGRPCCONTRACT._serialized_end=194
  _CONFIRMGRPCMODEL._serialized_start=197
  _CONFIRMGRPCMODEL._serialized_end=326
  _EXTERNALDATAGRPCMODEL._serialized_start=328
  _EXTERNALDATAGRPCMODEL._serialized_end=379
  _GETBYEMAILREQUEST._serialized_start=381
  _GETBYEMAILREQUEST._serialized_end=415
  _GETBYIDREQUEST._serialized_start=417
  _GETBYIDREQUEST._serialized_end=445
  _GETBYIDSREQUEST._serialized_start=447
  _GETBYIDSREQUEST._serialized_end=477
  _GETBYPHONEREQUEST._serialized_start=479
  _GETBYPHONEREQUEST._serialized_end=513
  _GETPERSONALDATABYSTATUSREQUEST._serialized_start=515
  _GETPERSONALDATABYSTATUSREQUEST._serialized_end=611
  _GETPERSONALDATABYSTATUSRESPONSE._serialized_start=613
  _GETPERSONALDATABYSTATUSRESPONSE._serialized_end=724
  _GETREQUEST._serialized_start=726
  _GETREQUEST._serialized_end=769
  _GETTOTALRESPONSE._serialized_start=771
  _GETTOTALRESPONSE._serialized_end=817
  _PERSONALDATABATCHRESPONSECONTRACT._serialized_start=819
  _PERSONALDATABATCHRESPONSECONTRACT._serialized_end=927
  _PERSONALDATAGRPCMODEL._serialized_start=930
  _PERSONALDATAGRPCMODEL._serialized_end=1656
  _PERSONALDATAGRPCRESPONSECONTRACT._serialized_start=1658
  _PERSONALDATAGRPCRESPONSECONTRACT._serialized_end=1764
  _REGISTERPERSONALDATAGRPCMODEL._serialized_start=1767
  _REGISTERPERSONALDATAGRPCMODEL._serialized_end=1977
  _RESULTGRPCRESPONSE._serialized_start=1979
  _RESULTGRPCRESPONSE._serialized_end=2011
  _SEARCHREQUEST._serialized_start=2013
  _SEARCHREQUEST._serialized_end=2048
  _UPDATEKYCGRPCCONTRACT._serialized_start=2051
  _UPDATEKYCGRPCCONTRACT._serialized_end=2214
  _UPDATEPERSONALDATAGRPCCONTRACT._serialized_start=2217
  _UPDATEPERSONALDATAGRPCCONTRACT._serialized_end=2605
  _PERSONALDATASERVICEGRPC._serialized_start=2756
  _PERSONALDATASERVICEGRPC._serialized_end=4191
# @@protoc_insertion_point(module_scope)
