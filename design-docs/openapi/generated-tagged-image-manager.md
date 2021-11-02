---
title: Tagged Image Manager v1.0.0
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="tagged-image-manager">Tagged Image Manager v1.0.0</h1>

> Scroll down for example requests and responses.

Base URLs:

* <a href="http://PENDING/v1">http://PENDING/v1</a>

# Authentication

<h1 id="tagged-image-manager-images">images</h1>

## listImages

<a id="opIdlistImages"></a>

> Code samples

`GET /images`

*List all Images*

Returns all images, newest created ones first.

<h3 id="listimages-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|end_timestamp|query|integer(int32)|false|Look for records created on or before this timestamp, in seconds since Unix Epoch|
|limit|query|integer(int32)|false|How many items to return at one time (max 100)|
|page|query|integer(int32)|false|Result page to return, 0 indexed|
|start_timestamp|query|integer(int32)|false|Look for records created on or after this timestamp, in seconds since Unix Epoch|
|uploaded_only|query|boolean|false|Only include records where the actual image file is present|

> Example responses

> 200 Response

```json
{
  "results": [
    {
      "id": 0,
      "created_by": "string",
      "created_timestamp": 0,
      "filename": "string",
      "size": 0,
      "tags": [
        {
          "id": 0,
          "name": "string"
        }
      ],
      "uploaded_timestamp": 0,
      "url": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}
```

<h3 id="listimages-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|A paged array of Images|[ImageBrowsePage](#schemaimagebrowsepage)|

<aside class="success">
This operation does not require authentication
</aside>

## createImage

<a id="opIdcreateImage"></a>

> Code samples

`POST /images`

*Create an Image Record, without uploading the Image*

> Body parameter

```json
{
  "filename": "string",
  "size": 0,
  "tags": [
    "string"
  ]
}
```

<h3 id="createimage-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ImageCreateInput](#schemaimagecreateinput)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "upload_url": "string"
}
```

<h3 id="createimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|ID of new record along with URL to upload (PUT) the image to.|[ImageCreatedResponse](#schemaimagecreatedresponse)|
|default|Default|unexpected error|[Error](#schemaerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getImage

<a id="opIdgetImage"></a>

> Code samples

`GET /images/{image_id}`

*Get an individual Image Record*

> Example responses

> 200 Response

```json
{
  "id": 0,
  "created_by": "string",
  "created_timestamp": 0,
  "filename": "string",
  "size": 0,
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "uploaded_timestamp": 0,
  "url": "string"
}
```

<h3 id="getimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An image record|[ImageRecord](#schemaimagerecord)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteImage

<a id="opIddeleteImage"></a>

> Code samples

`DELETE /images/{image_id}`

*Delete an individual Image Record*

<h3 id="deleteimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|Null response|None|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="tagged-image-manager-tags">tags</h1>

## listTags

<a id="opIdlistTags"></a>

> Code samples

`GET /tags`

*List all tags*

Returns all tags, in alphabetical order

<h3 id="listtags-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|limit|query|integer(int32)|false|How many items to return at one time (max 100)|
|page|query|integer(int32)|false|Result page to return, 0 indexed|

> Example responses

> 200 Response

```json
{
  "results": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}
```

<h3 id="listtags-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|A paged array of tags|[TagBrowsePage](#schematagbrowsepage)|

<aside class="success">
This operation does not require authentication
</aside>

## createTag

<a id="opIdcreateTag"></a>

> Code samples

`POST /tags`

*Create an Tag Record*

> Body parameter

```json
{
  "name": "string"
}
```

<h3 id="createtag-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[TagCreateInput](#schematagcreateinput)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "upload_url": "string"
}
```

<h3 id="createtag-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|ID of new record along with URL to upload (PUT) the image to.|[ImageCreatedResponse](#schemaimagecreatedresponse)|
|default|Default|unexpected error|[Error](#schemaerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getImage

<a id="opIdgetImage"></a>

> Code samples

`GET /tags/{tag_id}/images`

*Get images associated with a Tag Record*

> Example responses

> 200 Response

```json
{
  "results": [
    {
      "id": 0,
      "created_by": "string",
      "created_timestamp": 0,
      "filename": "string",
      "size": 0,
      "tags": [
        {
          "id": 0,
          "name": "string"
        }
      ],
      "uploaded_timestamp": 0,
      "url": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}
```

<h3 id="getimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An page of image records|[ImageBrowsePage](#schemaimagebrowsepage)|

<aside class="success">
This operation does not require authentication
</aside>

## deleteImage

<a id="opIddeleteImage"></a>

> Code samples

`DELETE /tags/{tag_id}`

*Delete an individual Tag Record*

Does not delete associated images

<h3 id="deleteimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|Null response|None|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="tagged-image-manager-search">search</h1>

## searchImages

<a id="opIdsearchImages"></a>

> Code samples

`GET /search/images`

*Search for images created within date range having one or more tags. Newest images are returned first.*

<h3 id="searchimages-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|end_timestamp|query|integer(int32)|false|Look for records created on or before this timestamp, in seconds since Unix Epoch|
|limit|query|integer(int32)|false|How many items to return at one time (max 100)|
|page|query|integer(int32)|false|Result page to return, 0 indexed|
|start_timestamp|query|integer(int32)|false|Look for records created on or after this timestamp, in seconds since Unix Epoch|
|exact_tags|query|array[string]|true|One or more exact tags (case sensitive) which must be present on the image, pipe delimited.|
|match_tags|query|array[string]|true|One or more tags which must match on the image, case insensitive, supports `%` as wildcard, pipe delimited.|
|uploaded_only|query|boolean|false|Only include records where the actual image file is present|

> Example responses

> 200 Response

```json
{
  "results": [
    {
      "id": 0,
      "created_by": "string",
      "created_timestamp": 0,
      "filename": "string",
      "size": 0,
      "tags": [
        {
          "id": 0,
          "name": "string"
        }
      ],
      "uploaded_timestamp": 0,
      "url": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}
```

<h3 id="searchimages-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An page of image records|[ImageBrowsePage](#schemaimagebrowsepage)|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="tagged-image-manager-upload">upload</h1>

## uploadImage

<a id="opIduploadImage"></a>

> Code samples

`POST /upload`

*Upload an Image and create an Image Record in one shot.*

Use this endpoint to upload images less then ~ 3.5MB and create records in one shot.

> Body parameter

```json
{
  "filename": "string",
  "image_data": "string",
  "tags": [
    "string"
  ]
}
```

<h3 id="uploadimage-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UploadCreateInput](#schemauploadcreateinput)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "upload_url": "string"
}
```

<h3 id="uploadimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|ID of new record along with URL to upload (PUT) the image to.|[ImageCreatedResponse](#schemaimagecreatedresponse)|
|default|Default|unexpected error|[Error](#schemaerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_ImageCreateInput">ImageCreateInput</h2>
<!-- backwards compatibility -->
<a id="schemaimagecreateinput"></a>
<a id="schema_ImageCreateInput"></a>
<a id="tocSimagecreateinput"></a>
<a id="tocsimagecreateinput"></a>

```json
{
  "filename": "string",
  "size": 0,
  "tags": [
    "string"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|filename|string|false|none|none|
|size|integer|false|none|none|
|tags|[string]|false|none|none|

<h2 id="tocS_ImageCreatedResponse">ImageCreatedResponse</h2>
<!-- backwards compatibility -->
<a id="schemaimagecreatedresponse"></a>
<a id="schema_ImageCreatedResponse"></a>
<a id="tocSimagecreatedresponse"></a>
<a id="tocsimagecreatedresponse"></a>

```json
{
  "id": 0,
  "upload_url": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|upload_url|string|false|none|Presigned s3 URL to PUT the image to.|

<h2 id="tocS_ImageUpdateInput">ImageUpdateInput</h2>
<!-- backwards compatibility -->
<a id="schemaimageupdateinput"></a>
<a id="schema_ImageUpdateInput"></a>
<a id="tocSimageupdateinput"></a>
<a id="tocsimageupdateinput"></a>

```json
{
  "tags": [
    "string"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|tags|[string]|false|none|none|

<h2 id="tocS_ImageRecord">ImageRecord</h2>
<!-- backwards compatibility -->
<a id="schemaimagerecord"></a>
<a id="schema_ImageRecord"></a>
<a id="tocSimagerecord"></a>
<a id="tocsimagerecord"></a>

```json
{
  "id": 0,
  "created_by": "string",
  "created_timestamp": 0,
  "filename": "string",
  "size": 0,
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "uploaded_timestamp": 0,
  "url": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|created_by|string|false|none|User or system which created this record|
|created_timestamp|integer|false|none|Creation time of record in seconds since Epoch|
|filename|string|false|none|none|
|size|integer|false|none|none|
|tags|[[Tag](#schematag)]|false|none|none|
|uploaded_timestamp|integer¦null|false|none|Upload time of related image in seconds since Epoch|
|url|string¦null|false|none|If the image has been uploaded, a time-limited pre-signed URL which can be used to retrieve it.|

<h2 id="tocS_ImageRecords">ImageRecords</h2>
<!-- backwards compatibility -->
<a id="schemaimagerecords"></a>
<a id="schema_ImageRecords"></a>
<a id="tocSimagerecords"></a>
<a id="tocsimagerecords"></a>

```json
[
  {
    "id": 0,
    "created_by": "string",
    "created_timestamp": 0,
    "filename": "string",
    "size": 0,
    "tags": [
      {
        "id": 0,
        "name": "string"
      }
    ],
    "uploaded_timestamp": 0,
    "url": "string"
  }
]

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[ImageRecord](#schemaimagerecord)]|false|none|none|

<h2 id="tocS_ImageBrowsePage">ImageBrowsePage</h2>
<!-- backwards compatibility -->
<a id="schemaimagebrowsepage"></a>
<a id="schema_ImageBrowsePage"></a>
<a id="tocSimagebrowsepage"></a>
<a id="tocsimagebrowsepage"></a>

```json
{
  "results": [
    {
      "id": 0,
      "created_by": "string",
      "created_timestamp": 0,
      "filename": "string",
      "size": 0,
      "tags": [
        {
          "id": 0,
          "name": "string"
        }
      ],
      "uploaded_timestamp": 0,
      "url": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|results|[ImageRecords](#schemaimagerecords)|false|none|none|
|meta|[PageMeta](#schemapagemeta)|false|none|none|

<h2 id="tocS_Tag">Tag</h2>
<!-- backwards compatibility -->
<a id="schematag"></a>
<a id="schema_Tag"></a>
<a id="tocStag"></a>
<a id="tocstag"></a>

```json
{
  "id": 0,
  "name": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|name|string|true|none|none|

<h2 id="tocS_Tags">Tags</h2>
<!-- backwards compatibility -->
<a id="schematags"></a>
<a id="schema_Tags"></a>
<a id="tocStags"></a>
<a id="tocstags"></a>

```json
[
  {
    "id": 0,
    "name": "string"
  }
]

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Tag](#schematag)]|false|none|none|

<h2 id="tocS_TagBrowsePage">TagBrowsePage</h2>
<!-- backwards compatibility -->
<a id="schematagbrowsepage"></a>
<a id="schema_TagBrowsePage"></a>
<a id="tocStagbrowsepage"></a>
<a id="tocstagbrowsepage"></a>

```json
{
  "results": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "meta": {
    "current_page": 0,
    "has_more_pages": true,
    "total_results": 0
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|results|[Tags](#schematags)|false|none|none|
|meta|[PageMeta](#schemapagemeta)|false|none|none|

<h2 id="tocS_TagCreateInput">TagCreateInput</h2>
<!-- backwards compatibility -->
<a id="schematagcreateinput"></a>
<a id="schema_TagCreateInput"></a>
<a id="tocStagcreateinput"></a>
<a id="tocstagcreateinput"></a>

```json
{
  "name": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|false|none|none|

<h2 id="tocS_TagUpdateInput">TagUpdateInput</h2>
<!-- backwards compatibility -->
<a id="schematagupdateinput"></a>
<a id="schema_TagUpdateInput"></a>
<a id="tocStagupdateinput"></a>
<a id="tocstagupdateinput"></a>

```json
{
  "name": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|false|none|none|

<h2 id="tocS_UploadCreateInput">UploadCreateInput</h2>
<!-- backwards compatibility -->
<a id="schemauploadcreateinput"></a>
<a id="schema_UploadCreateInput"></a>
<a id="tocSuploadcreateinput"></a>
<a id="tocsuploadcreateinput"></a>

```json
{
  "filename": "string",
  "image_data": "string",
  "tags": [
    "string"
  ]
}

```

Input to combination upload endpoint. Entire payload must not exceed 3.96 MB.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|filename|string|false|none|none|
|image_data|string(byte)|false|none|Base 64 encoded image data|
|tags|[string]|false|none|none|

<h2 id="tocS_PageMeta">PageMeta</h2>
<!-- backwards compatibility -->
<a id="schemapagemeta"></a>
<a id="schema_PageMeta"></a>
<a id="tocSpagemeta"></a>
<a id="tocspagemeta"></a>

```json
{
  "current_page": 0,
  "has_more_pages": true,
  "total_results": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|current_page|integer|false|none|none|
|has_more_pages|boolean|false|none|none|
|total_results|integer|false|none|none|

<h2 id="tocS_Error">Error</h2>
<!-- backwards compatibility -->
<a id="schemaerror"></a>
<a id="schema_Error"></a>
<a id="tocSerror"></a>
<a id="tocserror"></a>

```json
{
  "code": 0,
  "message": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer(int32)|true|none|none|
|message|string|true|none|none|

