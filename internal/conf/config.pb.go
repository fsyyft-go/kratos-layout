// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.6
// 	protoc        v5.29.3
// source: internal/conf/config.proto

package conf

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	durationpb "google.golang.org/protobuf/types/known/durationpb"
	reflect "reflect"
	sync "sync"
	unsafe "unsafe"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// Config 定义应用程序的配置结构，包含所有子系统的配置信息。
type Config struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// Log 配置应用程序的日志系统。
	Log *Log `protobuf:"bytes,1,opt,name=log,proto3" json:"log,omitempty"`
	// Server 配置应用程序的服务器设置。
	Server        *Server `protobuf:"bytes,2,opt,name=server,proto3" json:"server,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Config) Reset() {
	*x = Config{}
	mi := &file_internal_conf_config_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Config) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Config) ProtoMessage() {}

func (x *Config) ProtoReflect() protoreflect.Message {
	mi := &file_internal_conf_config_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Config.ProtoReflect.Descriptor instead.
func (*Config) Descriptor() ([]byte, []int) {
	return file_internal_conf_config_proto_rawDescGZIP(), []int{0}
}

func (x *Config) GetLog() *Log {
	if x != nil {
		return x.Log
	}
	return nil
}

func (x *Config) GetServer() *Server {
	if x != nil {
		return x.Server
	}
	return nil
}

// Log 定义日志系统的详细配置参数。
type Log struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// type 指定日志系统类型，支持 logrus 等日志框架。
	Type string `protobuf:"bytes,1,opt,name=type,proto3" json:"type,omitempty"`
	// output 指定日志输出的目标路径，可以是文件路径或特殊值（如 stdout）。
	Output string `protobuf:"bytes,2,opt,name=output,proto3" json:"output,omitempty"`
	// level 指定日志记录的级别，可选值包括：debug、info、warn、error。
	Level         string `protobuf:"bytes,3,opt,name=level,proto3" json:"level,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Log) Reset() {
	*x = Log{}
	mi := &file_internal_conf_config_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Log) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Log) ProtoMessage() {}

func (x *Log) ProtoReflect() protoreflect.Message {
	mi := &file_internal_conf_config_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Log.ProtoReflect.Descriptor instead.
func (*Log) Descriptor() ([]byte, []int) {
	return file_internal_conf_config_proto_rawDescGZIP(), []int{1}
}

func (x *Log) GetType() string {
	if x != nil {
		return x.Type
	}
	return ""
}

func (x *Log) GetOutput() string {
	if x != nil {
		return x.Output
	}
	return ""
}

func (x *Log) GetLevel() string {
	if x != nil {
		return x.Level
	}
	return ""
}

// Server 定义服务器相关的配置参数。
type Server struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Server) Reset() {
	*x = Server{}
	mi := &file_internal_conf_config_proto_msgTypes[2]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Server) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Server) ProtoMessage() {}

func (x *Server) ProtoReflect() protoreflect.Message {
	mi := &file_internal_conf_config_proto_msgTypes[2]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Server.ProtoReflect.Descriptor instead.
func (*Server) Descriptor() ([]byte, []int) {
	return file_internal_conf_config_proto_rawDescGZIP(), []int{2}
}

// HTTP 定义 HTTP 服务器的配置参数。
type Server_HTTP struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// network 指定网络类型，如 tcp、tcp4、tcp6 等。
	Network string `protobuf:"bytes,1,opt,name=network,proto3" json:"network,omitempty"`
	// addr 指定服务器监听的地址和端口，格式为 host:port。
	Addr string `protobuf:"bytes,2,opt,name=addr,proto3" json:"addr,omitempty"`
	// timeout 定义 HTTP 请求的超时时间。
	Timeout       *durationpb.Duration `protobuf:"bytes,3,opt,name=timeout,proto3" json:"timeout,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Server_HTTP) Reset() {
	*x = Server_HTTP{}
	mi := &file_internal_conf_config_proto_msgTypes[3]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Server_HTTP) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Server_HTTP) ProtoMessage() {}

func (x *Server_HTTP) ProtoReflect() protoreflect.Message {
	mi := &file_internal_conf_config_proto_msgTypes[3]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Server_HTTP.ProtoReflect.Descriptor instead.
func (*Server_HTTP) Descriptor() ([]byte, []int) {
	return file_internal_conf_config_proto_rawDescGZIP(), []int{2, 0}
}

func (x *Server_HTTP) GetNetwork() string {
	if x != nil {
		return x.Network
	}
	return ""
}

func (x *Server_HTTP) GetAddr() string {
	if x != nil {
		return x.Addr
	}
	return ""
}

func (x *Server_HTTP) GetTimeout() *durationpb.Duration {
	if x != nil {
		return x.Timeout
	}
	return nil
}

var File_internal_conf_config_proto protoreflect.FileDescriptor

const file_internal_conf_config_proto_rawDesc = "" +
	"\n" +
	"\x1ainternal/conf/config.proto\x12\rinternal.conf\x1a\x1egoogle/protobuf/duration.proto\"]\n" +
	"\x06Config\x12$\n" +
	"\x03log\x18\x01 \x01(\v2\x12.internal.conf.LogR\x03log\x12-\n" +
	"\x06server\x18\x02 \x01(\v2\x15.internal.conf.ServerR\x06server\"G\n" +
	"\x03Log\x12\x12\n" +
	"\x04type\x18\x01 \x01(\tR\x04type\x12\x16\n" +
	"\x06output\x18\x02 \x01(\tR\x06output\x12\x14\n" +
	"\x05level\x18\x03 \x01(\tR\x05level\"s\n" +
	"\x06Server\x1ai\n" +
	"\x04HTTP\x12\x18\n" +
	"\anetwork\x18\x01 \x01(\tR\anetwork\x12\x12\n" +
	"\x04addr\x18\x02 \x01(\tR\x04addr\x123\n" +
	"\atimeout\x18\x03 \x01(\v2\x19.google.protobuf.DurationR\atimeoutB7Z5github.com/fsyyft-go/kratos-layout/internal/conf;confb\x06proto3"

var (
	file_internal_conf_config_proto_rawDescOnce sync.Once
	file_internal_conf_config_proto_rawDescData []byte
)

func file_internal_conf_config_proto_rawDescGZIP() []byte {
	file_internal_conf_config_proto_rawDescOnce.Do(func() {
		file_internal_conf_config_proto_rawDescData = protoimpl.X.CompressGZIP(unsafe.Slice(unsafe.StringData(file_internal_conf_config_proto_rawDesc), len(file_internal_conf_config_proto_rawDesc)))
	})
	return file_internal_conf_config_proto_rawDescData
}

var file_internal_conf_config_proto_msgTypes = make([]protoimpl.MessageInfo, 4)
var file_internal_conf_config_proto_goTypes = []any{
	(*Config)(nil),              // 0: internal.conf.Config
	(*Log)(nil),                 // 1: internal.conf.Log
	(*Server)(nil),              // 2: internal.conf.Server
	(*Server_HTTP)(nil),         // 3: internal.conf.Server.HTTP
	(*durationpb.Duration)(nil), // 4: google.protobuf.Duration
}
var file_internal_conf_config_proto_depIdxs = []int32{
	1, // 0: internal.conf.Config.log:type_name -> internal.conf.Log
	2, // 1: internal.conf.Config.server:type_name -> internal.conf.Server
	4, // 2: internal.conf.Server.HTTP.timeout:type_name -> google.protobuf.Duration
	3, // [3:3] is the sub-list for method output_type
	3, // [3:3] is the sub-list for method input_type
	3, // [3:3] is the sub-list for extension type_name
	3, // [3:3] is the sub-list for extension extendee
	0, // [0:3] is the sub-list for field type_name
}

func init() { file_internal_conf_config_proto_init() }
func file_internal_conf_config_proto_init() {
	if File_internal_conf_config_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: unsafe.Slice(unsafe.StringData(file_internal_conf_config_proto_rawDesc), len(file_internal_conf_config_proto_rawDesc)),
			NumEnums:      0,
			NumMessages:   4,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_internal_conf_config_proto_goTypes,
		DependencyIndexes: file_internal_conf_config_proto_depIdxs,
		MessageInfos:      file_internal_conf_config_proto_msgTypes,
	}.Build()
	File_internal_conf_config_proto = out.File
	file_internal_conf_config_proto_goTypes = nil
	file_internal_conf_config_proto_depIdxs = nil
}
