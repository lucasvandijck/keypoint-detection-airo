import os
import unittest

import numpy as np

from keypoint_detection.data.dataset import KeypointsDataset, KeypointsDatasetPreloaded


class TestDataSet(unittest.TestCase):
    def setUp(self):
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(TEST_DIR, "test_dataset/dataset.json")
        self.image_path = os.path.join(TEST_DIR, "test_dataset")
        self.keypoint_channels = "  flap_corner_keypoints corner_keypoints  "
        self.channel_max_keypoints = " -1 -1  "

    def test_dataset(self):

        dataset = KeypointsDataset(self.json_path, self.image_path, self.keypoint_channels, self.channel_max_keypoints)
        item = dataset.__getitem__(0)
        img, keypoints = item

        self.assertEqual(len(keypoints), 2)
        flap, corner = keypoints
        self.assertEqual(img.shape, (3, 64, 64))
        self.assertEqual(len(corner), 4)
        self.assertEqual(len(flap), 8)

        dataset = KeypointsDataset(
            self.json_path,
            self.image_path,
            ["corner_keypoints", "flap_corner_keypoints", "flap_corner_keypoints_visible"],
            [4, 8, 8],
        )
        item = dataset.__getitem__(0)
        img, keypoints = item
        self.assertEqual(len(keypoints), 3)
        corner, flap, flap_visible = keypoints
        self.assertEqual(len(flap_visible), 8)


class TestDatasetPreloader(unittest.TestCase):
    def setUp(self):
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(TEST_DIR, "test_dataset/dataset.json")
        self.image_path = os.path.join(TEST_DIR, "test_dataset")

    def test_preloader(self):
        preloadeded_dataset = KeypointsDatasetPreloaded(
            self.json_path,
            self.image_path,
            n_io_attempts=2,
            keypoint_channels="corner_keypoints",
            keypoint_channel_max_keypoints="-1",
        )
        self.assertEqual(len(preloadeded_dataset.__getitem__(1)), 2)
        self.assertIsNotNone(preloadeded_dataset.preloaded_images[0])
        self.assertTrue(isinstance(preloadeded_dataset.preloaded_images[0], np.ndarray))
        self.assertEqual(preloadeded_dataset.preloaded_images[0].dtype, np.uint8)
