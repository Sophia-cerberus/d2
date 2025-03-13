
# 文件存储和处理服务使用指南

## 服务概述

本服务是基于 **Django** 和 **Django REST Framework** 构建的文件存储和处理系统，旨在提供图片文件的上传、存储、处理（如生成缩略图）、下载和删除等功能。本服务支持 **jpg、jpeg、png** 格式的图片文件，并通过 **Pillow** 库进行图片处理。

---

## 技术架构

- **Web 框架**：Django
- **RESTful API**：Django REST Framework (DRF)
- **图片处理**：Pillow (PIL)
- **存储方式**：本地文件系统（可扩展为云存储）
- **数据库**：SQLite（用于存储文件元数据）

---

## 目录结构

```
storage/
├── apps/storage
│   ├── __init__.py
│   ├── models
│   ├── serializers
│   ├── filter
|   ├── tests
|   ├── views
|   ├── urls.py
│   └── app.py

│
├── media/
│   └── <:pk>
|         ├──origin
|         └──thumb
│
├── manage.py
│
├── db
│   └── db.sqlite3
│
├── protocol
|   ├── asgi.py
|   └── wsgi.py
|
├── router
|   └── urls.py
|
├── settings
|   └── base.py
|
├── utils
|   └── ...
```

---

## 1. **安装与配置**

### 1.1 **安装依赖**

首先，确保您的开发环境已安装 Python 3.x。然后，使用以下命令安装所需的依赖：

```bash
pip install Django djangorestframework Pillow django-cos-header
```

### 1.2 **配置 Django 项目**

在 `settings.py` 中配置文件存储和认证：

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storage.apps.StorageConfig',

    'drf_yasg',
    'rest_framework',
    'corsheaders',
]

# 文件存储配置
if not os.path.exists(os.path.join(BASE_DIR, 'media')):
    os.makedirs(os.path.join(BASE_DIR, 'media'))

# 访问上传文件的url地址前缀
MEDIA_URL = "/media/"
# 项目中存储上传文件的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
```

### 1.3 **迁移数据库**

执行数据库迁移操作：

```bash
python manage.py makemigrations storage
python manage.py migrate
```

---

## 2. **API 接口说明**

### 2.1 **上传文件**

- **方法**：`POST`
- **接口地址**：`/api/v1/storage/media/`
- **请求参数**：
  - `file`: 上传的图片文件（支持 `jpg`、`jpeg`、`png` 格式）
  - `Authorization`: API 密钥（格式：`Basic your-api-key`）

#### 示例请求：

```bash
curl -X POST -F "file=@path_to_image.jpg" -H "Basic: Basic your-api-key" http://127.0.0.1:8000/api/v1/storage/media/
```

#### 返回示例：

```json
{
    "file":"http://localhost:8000/media/oTxLxyYu/origin/jpg_44-2_oTxLxyYu.jpg",
    "width":2400,
    "height":1599,
    "size":373507,
    "thumb":"http://localhost:8000/media/oTxLxyYu/thumb/jpg_44-2_oTxLxyYu.jpg"
}
```

---

### 2.2 **查看已上传文件列表**

- **方法**：`GET`
- **接口地址**：`/api/v1/storage/media/`
- **请求参数**：
  - `Authorization`: API 密钥

#### 示例请求：
```bash
curl -X GET -H "Basic: Basic your-api-key" http://127.0.0.1:8000/api/v1/storage/media/
```

#### 返回示例：

```json
{
  "code": 200,
  "data": {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": "nhVK9GX0",
        "file": "/media/nhVK9GX0/origin/jpg_44-2_nhVK9GX0..jpg",
        "thumb": "/media/nhVK9GX0/thumb/jpg_44-2_nhVK9GX0..jpg",
        "name": "",
        "size": 373507,
        "width": 2400,
        "height": 1599
      },
    ]
  },
  "message": "success",
  "status": "success"
}
```

---

### 2.3 **下载文件**
直接访问列表或详情接口文件地址

---

### 2.4 **下载缩略图**
直接访问列表或详情接口文件地址

---

### 2.5 **删除文件**

- **方法**：`DELETE`
- **接口地址**：`/api/v1/storage/image/{id}/`
- **请求参数**：
  - `id`: 文件的唯一 ID
  - `Authorization`: API 密钥

#### 示例请求：

```bash
curl -X DELETE -H "Basic: Basic your-api-key" http://127.0.0.1:8000/api/v1/storage/media/{id}/
```

该请求将删除文件及其缩略图。

---

## 3. **文件上传限制**

- **支持文件格式**：仅支持 `.jpg`、`.jpeg`、`.png` 格式。
- **最大文件大小**：上传文件最大限制为 **5MB**。
- **缩略图生成**：文件上传成功后，系统会自动生成缩略图，缩略图尺寸为 **200x200** 像素，保持长宽比。

---

## 4. **用户认证**

本服务使用 **API 密钥** 进行用户认证。在每个请求中，用户需将其 API 密钥作为 Authorization 头传递。格式如下：

```
Authorization: Basic your-api-key
```

### 获取 API 密钥

- 用户可以在管理界面或通过注册 API 密钥来获得密钥。
- 密钥将用于身份验证，确保文件访问的安全性。

---

## 6. **总结**

本服务提供了一个简单高效的图片上传、存储、处理（如生成缩略图）和下载接口。通过简单的 API 请求，用户可以轻松管理自己的图片文件。如果您有任何问题或需要帮助，请通过邮件联系我们。

