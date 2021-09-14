from marshmallow import (
    Schema,
    fields,
    validate
)


class URLSchema(Schema):
    url = fields.URL(required=True,validate=[validate.Length(min=8, max=10000)])


class IdSchema(Schema):
    url_id = fields.String(required=True,validate=[validate.Length(min=1, max=30)])


class Surl_IDSchema(Schema):
    url_id = fields.String(required=True, validate=[validate.Length(min=1, max=30)])
    url = fields.URL(required=True,validate=[validate.Length(min=8, max=10000)])
