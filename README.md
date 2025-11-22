# 基于Python的USB PD报文解析通用API

![version](https://img.shields.io/badge/Versio-1.0.0-green)

## 项目介绍

该项目提供面向Python的USB PD报文解析的通用API，仅需要pip安装即可使用。

当前版本为正式版，可能存在许多问题，您可以向本项目反馈issue和提供PR，感谢您的支持。

## 支持 Support

**支持所有报文信息的全部解析。**

**Support the complete parsing of all message information.**

## 使用

推荐通过PyPI安装，仅需要在需要的环境中

```cmd
pip install usbpdparser
```

或从GitHub下载源文件解压，或是git clone

```cmd
cd USB_PD_Parser_API_Py
pip install .
```

本项目会自动安装成，在您的项目中导入

```python
import usbpdparser
```

即可开箱使用。

## 数据结构

请仔细阅读以下内容确保您能正确的调用API。

本项目推荐使用的接口仅metadata类和Parser类两个。

### 元数据 metadata类

任何经过解析的内容都将以元数据进行打包，元数据的基本结构如下

| 属性    | 类型  | 作用                                 |
| ------- | ----- | ------------------------------------ |
| raw     | str   | 当前元数据的二进制值                 |
| bit_loc | tuple | 当前元数据在上一层的比特位置         |
| field   | str   | 当前元数据字段名                     |
| value   | any   | 当前元数据字段值或是下一层元数据list |

您可以使用 `raw()` 、 `bit_loc()` 、 `field()` 、 `value()` 四个函数来调取他们的内容。

当您 `print()` 一个metadata类时，它将默认返回`value` 的内容；当您请求了metadata类的可重建描述时，它将默认返回 `field` : `value` 组成的字符串。

您可以对任意 `value` 为元数据list的元数据使用[index]或[field]来获取list中的元数据，其中field为想要获取的元数据的 `field` 。

额外提供 `quick_pdo()` 、 `quick_rdo()` 、 `pdo()` 、 `full_raw()` 、 `raw_value()` 五个函数来调取附加内容，其中 `quick_pdo()` 和 `quick_rdo()` 提供PDO和RDO短预览， `pdo()` 提供RDO报文中所选的PDO， `full_raw()` 返回extend message消息中当前拼接好的raw， `raw_value()` 返回extend message消息中本报文的raw（此时的 `value()` 返回的是拼接后的 `value` ）

### Parser类

若要使用流式解析PD报文，需要您创建 `Parser` 类实例，其提供一种方法。

`parse(sop, raw, verify_crc, last_pdo, last_ext, last_rdo)` 方法将解析PD报文， `sop` 为该条报文的SOP信息， `raw` 可以是uint8 list、str、int、bytes中的任意一种， `verify_crc` 如果为True则会校验CRC是否正确。如果您同时不提供 `last_pdo` 、 `last_ext` 、 `last_rdo` 参数则默认解析实例内保存的报文，返回解析完的元数据。如您提供 `last_pdo` 、 `last_ext` 、 `last_rdo` 其中任一参数则会以提供的为准（为提供的为None），其中 `last_pdo` 为可能的Request消息提供PDO信息， `last_ext` 为可能的分包的Extended消息提供上下文， `last_rdo` 为可能的Status消息提供RDO信息。

### 一些工具函数

本项目还提供四个工具函数，分别是 `is_pdo(msg)` 、 `is_rdo(msg)` 、 `provide_ext(msg)` 、 `render(data)` 。

#### is_pdo(msg)

该函数接收一个metadata类，判断其是否是一个PDO报文，返回bool类型。

#### is_rdo(msg)

该函数接收一个metadata类，判断其是否是一个RDO报文，返回bool类型。

#### provide_ext(msg)

该函数接收一个metadata类，判断其是否为有效的Extended消息的上下文，返回bool类型。

#### render(data)

该函数接收一个metadata类或是metadata类为元素的list，返回一个元素为（color style, text）的元组，其中text包含换行信息，直接使用无换行打印即可预览metadata。
