
"""
对于一个CodeObject来说，一个对象（函数）被转换为CodeObject属于 被编译 assemble 成为一个结构体 ADO(AssembledDataObject)
如果一个ADO被序列化为bytes，属于被序列化（Serialized）
此时是一个bytes对象

一个bytes对象被反序列化为ADO
ADO再被反编译为CodeObject
CodeObject再运行

那么在这种情况下，界面需要给出的就仅是对bytes的传输进行加解密

"""

"""
描述如下：
                                            ┌──────────────┐
                                            │              │
                                            │  Exec        │
                                            └───────▲──────┘
                                                    │
┌────────────────┐                                  │      runtime
│                │                                  │
│  Python Object │                                  │
│   (Function)   │                          ┌───────┴───────┐
│                │                          │               │
└───────┬────────┘                          │               │
        │                                   │ Python Object │
        │                                   │               │
        │  Assemble                         └──────▲────────┘
        │                                          │      Disassemble
        │            ▼                             │
        │                                          │
┌───────▼─────────┐                      ┌─────────┴──────┐
│ CodeObject      │                      │                │
│ CertionVersion  │                      │   CodeObject   │
│                 │                      │                │
└────────┬────────┘                      └─────────▲──────┘
         │                                         │
         │Serialized                               │
         │                                         │      Deserialized
         ▼                                         │
 ┌─────────────────┐                      ┌────────┴──────┐
 │ Object          │                      │               │
 │ PickleVersion   │                      │  BinObject    │
 │                 │                      │               │
 └────────┬────────┘                      └───────────────┘
          │                                      ▲
          │  Encryption                          │       Decryption
          ▼                                      │
┌────────────────────────────────────────────────┴─────────────────────┐
│                                                                      │
│                       Bytes Sequences                                │
└──────────────────────────────────────────────────────────────────────┘

"""