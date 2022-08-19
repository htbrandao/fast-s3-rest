import boto3
import unittest

from fast_s3_rest.modulo import _client, _resource, _bucket, _representacoes, params


class TesteObjetosS3Params(unittest.TestCase):

    def test_params(self):
        self.assertIsInstance(params, dict)


class TesteObjetosS3Client(unittest.TestCase):

    def test_client(self):
        _1 = _client()
        _2 = boto3.client('s3')
        self.assertEqual(str(type(_1)), str(type(_2)))


class TesteObjetosS3Resource(unittest.TestCase):

    def test_resource(self):
        _1 = _resource()
        _2 = boto3.resource('s3')
        self.assertEqual(str(type(_1)), str(type(_2)))


class TesteObjetosS3Bucket(unittest.TestCase):

    def test_bucket(self):
        _1 = _bucket()
        _2 = boto3.resource('s3').Bucket('nome_bucket')
        self.assertEqual(str(type(_1)), str(type(_2)))


class TesteObjetosS3Representacoes(unittest.TestCase):

    r = _representacoes()

    def test_representacoes(self):
        _a1 = self.r[0]
        _a2 = boto3.client('s3')
        _b1 = self.r[1]
        _b2 = boto3.resource('s3')
        _c1 = self.r[2]
        _c2 = boto3.resource('s3').Bucket('nome_bucket')
        self.assertEqual(str(type(_a1)), str(type(_a2)))
        self.assertEqual(str(type(_b1)), str(type(_b2)))
        self.assertEqual(str(type(_c1)), str(type(_c2)))
