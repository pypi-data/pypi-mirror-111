import binascii
import logging

import aws_encryption_sdk
import boto3
from config.settings.base import MESSAGING_TEMPLATE_BUCKET

from buildblock.apps.messaging.models import MessagingTemplates
from buildblock.settings import BLOCKCHAIN_KEY_ARN, BLOCKCHAIN_KEY_BUCKET

logger = logging.getLogger(__name__)


class AwsService:
    kms_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(key_ids=[BLOCKCHAIN_KEY_ARN])
    s3 = boto3.resource('s3')

    @classmethod
    def _encrypt(cls, plaintext):
        """Encryption and decryption for storing in S3"""
        ciphertext, _ = aws_encryption_sdk.encrypt(
            source=plaintext,
            key_provider=cls.kms_key_provider
        )
        return ciphertext

    @classmethod
    def _decrypt(cls, ciphertext):
        cycled_plaintext, _ = aws_encryption_sdk.decrypt(
            source=ciphertext,
            key_provider=cls.kms_key_provider
        )
        return cycled_plaintext.decode()

    @classmethod
    def encrypt_personal_info(cls, plaintext):
        """Encryption and decryption for personal info. stored in DB"""
        return cls._encrypt(plaintext).hex()

    @classmethod
    def decrypt_personal_info(cls, ciphertext):
        return cls._decrypt(binascii.unhexlify(ciphertext))

    @classmethod
    def store_user_key(cls, account_address, key):
        new_object = cls.s3.Object(BLOCKCHAIN_KEY_BUCKET, 'user/' + account_address)
        new_object.put(Body=cls._encrypt(key))

    @classmethod
    def get_user_key(cls, account_address):
        try:
            retrieved_object = cls.s3.Object(BLOCKCHAIN_KEY_BUCKET, 'user/' + account_address)
            return cls._decrypt(retrieved_object.get()['Body'].read())
        except Exception as e:
            print(str(e))
            return None

    @classmethod
    def put_messaging_template(cls, message_template_id: int, body: str) -> None:
        try:
            new_object = cls.s3.Object(MESSAGING_TEMPLATE_BUCKET, str(message_template_id))
            new_object.put(Body=body)
            return True
        except Exception as e:
            logger.error(f'Error has occurred while creating data: {e}')
            return False

    @classmethod
    def get_messaging_template(cls, message_template_id) -> str:
        try:
            retrieved_object = cls.s3.Object(MESSAGING_TEMPLATE_BUCKET, str(message_template_id))
            return retrieved_object.get()['Body'].read().decode('utf-8')
        except Exception as e:
            logger.error(f'Error has occurred while loading data: {e}')
            return False
