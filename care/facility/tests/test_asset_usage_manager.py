from unittest import mock

from rest_framework.test import APITestCase

from care.users.models import User
from care.utils.assetintegration.usage_manager import UsageManager
from care.utils.tests.test_utils import TestUtils


class UsageManagerTestCase(TestUtils, APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.state = cls.create_state()
        cls.district = cls.create_district(cls.state)
        cls.local_body = cls.create_local_body(cls.district)
        cls.super_user = cls.create_super_user("su", cls.district)
        cls.facility = cls.create_facility(cls.super_user, cls.district, cls.local_body)
        cls.asset_location = cls.create_asset_location(cls.facility)
        cls.asset = cls.create_asset(cls.asset_location)

    def setUp(self):
        self.user1 = self.create_user(
            username="test_user_1",
            state=self.state,
            district=self.district,
            user_type=User.TYPE_VALUE_MAP["StateAdmin"],
        )
        self.user2 = self.create_user(
            username="test_user_2",
            state=self.state,
            district=self.district,
            user_type=User.TYPE_VALUE_MAP["StateAdmin"],
        )

        self.mock_cache = mock.MagicMock()
        self.cache_patcher = mock.patch(
            "care.utils.assetintegration.usage_manager.cache", self.mock_cache
        )
        self.cache_patcher.start()

        self.usage_manager_user1 = UsageManager(
            asset_id=self.asset.external_id, user=self.user1
        )
        self.usage_manager_user2 = UsageManager(
            asset_id=self.asset.external_id, user=self.user2
        )

        self.mock_redis_client = mock.MagicMock()
        self.usage_manager_user1.redis_client = self.mock_redis_client
        self.usage_manager_user2.redis_client = self.mock_redis_client

    def tearDown(self):
        self.cache_patcher.stop()

    def test_has_access(self):
        self.mock_cache.get.return_value = None
        self.assertTrue(self.usage_manager_user1.has_access())

        self.mock_cache.get.return_value = self.user1.id
        self.assertTrue(self.usage_manager_user1.has_access())

        self.mock_cache.get.return_value = self.user2.id
        self.assertFalse(self.usage_manager_user1.has_access())

    def test_unlock_camera(self):
        self.mock_cache.get.return_value = self.user1.id

        with mock.patch.object(
            self.usage_manager_user1, "notify_waiting_list_on_asset_availabe"
        ) as mock_notify:
            self.usage_manager_user1.unlock_camera()

            self.mock_cache.delete.assert_called_once_with(
                self.usage_manager_user1.current_user_cache_key
            )

            mock_notify.assert_called_once()

    def test_request_access(self):
        self.mock_cache.get.return_value = None
        self.assertTrue(self.usage_manager_user1.request_access())

        self.mock_cache.get.return_value = self.user2.id
        with mock.patch(
            "care.utils.notification_handler.send_webpush"
        ) as mock_send_webpush:
            result = self.usage_manager_user1.request_access()
            self.assertFalse(result)
            mock_send_webpush.assert_called_once()

    def test_lock_camera(self):
        self.mock_cache.get.return_value = None
        self.assertTrue(self.usage_manager_user1.lock_camera())
        self.mock_cache.set.assert_called_once_with(
            self.usage_manager_user1.current_user_cache_key,
            self.user1.id,
            timeout=60 * 5,
        )

        self.mock_cache.get.return_value = self.user2.id
        self.assertFalse(self.usage_manager_user1.lock_camera())

    def test_current_user(self):
        self.mock_cache.get.return_value = self.user1.id

        mock_serializer = mock.MagicMock()
        mock_serializer.data = {
            "id": self.user1.id,
            "username": self.user1.username,
        }

        with mock.patch(
            "care.facility.api.serializers.asset.UserBaseMinimumSerializer",
            return_value=mock_serializer,
        ):
            current_user_data = self.usage_manager_user1.current_user()
            self.assertIsNotNone(current_user_data)
            self.assertEqual(current_user_data["id"], self.user1.id)
