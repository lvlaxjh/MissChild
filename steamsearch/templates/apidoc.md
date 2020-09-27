# 如何使用API

## 获取网站基本记录信息

- 请求类型：` post`

- 请求链接：` www.jhc.ccol/api/basicIinformation`

- 返回格式：`json`

  - `code`：`int`请求码

    | code返回内容 | 解释 |
    | ---- | -------- |
    | -1 | 请求报错 |
    | 1    | 成功请求 |

  - `basicinformation`：

    - `time`:`time`当前时间
    
  - `Total`：`dict`记录数据统计
      
    - `note`：`string`"失联人员统计信息数量”
    - `exist`:`string`已登记数量
      - `webInf`：`dict`网站信息
        - `note`：`string`"网站信息”
        - `visits`：`string`访问次数
        - `search`：`string`搜索次数
      - `upload`：`string`上传次数
    
  - `error`：`string`当code为-1时，返回报错信息

## 请求失联者信息

- 请求类型：`post`

- 请求链接：`www.jhc.cool/api/getinformation`

- post发送：`json`

  ```json
  {
  	"name":""//string-请求失联人员姓名
  }
  ```

  - 返回格式：`json`

    - `code`：`int`请求码

      | code返回内容 | 解释     |
      | ------------ | -------- |
      | -1           | 请求报错 |
      | 1            | 成功请求 |
      
    - `getinformation`：`dict`

      - `time`：`time`当前时间

      - `content`：`list`人员列表

        - `dict`一条信息

          - `name`：`string`姓名

          - sex：`string`性别

            | 性别代码 | 解释      |
            | -------- | --------- |
            | none     | 未知/其他 |
            | nan      | 男        |
            | nv       | 女        |

          - `birthday`：`time`出生日期

          - `heigt`：`string`身高

          - `weight`：`string`体重

          - `timeL`：`string`失联事件

          - `site`：`string`失联地点

          - `text`：`string`描述

          - `kinName`：`string`家属称呼

          - `kinLink`：`string`家属联系方式

          - `img`：`list`图片列表

            - `string`图片链接