import unittest
from spotr.availability_zone import AvailabilityZone


class TestAvailabilityZone(unittest.TestCase):
    def test_init(self):
        """Test AvailabilityZone initialization"""
        price_history = [{'SpotPrice': '0.05'}, {'SpotPrice': '0.06'}]
        az = AvailabilityZone('us-east-1a', price_history)
        
        self.assertEqual(az.zone_name, 'us-east-1a')
        self.assertEqual(az.price_history, price_history)

    def test_current_price_with_history(self):
        """Test current price property with price history"""
        price_history = [{'SpotPrice': '0.05'}, {'SpotPrice': '0.06'}]
        az = AvailabilityZone('us-east-1a', price_history)
        
        # Should return the first (most recent) price as float
        self.assertEqual(az.current_price, 0.05)

    def test_current_price_empty_history(self):
        """Test current price property with empty price history"""
        az = AvailabilityZone('us-east-1a', [])
        
        # Should return None for empty price history
        self.assertIsNone(az.current_price)

    def test_current_price_none_history(self):
        """Test current price property with None price history"""
        az = AvailabilityZone('us-east-1a', None)
        
        # Should return None for None price history
        self.assertIsNone(az.current_price)

    def test_repr_with_price(self):
        """Test string representation with price"""
        price_history = [{'SpotPrice': '0.123456'}]
        az = AvailabilityZone('us-west-2b', price_history)
        
        expected = "us-west-2b for $0.123456/hr"
        self.assertEqual(repr(az), expected)

    def test_repr_without_price(self):
        """Test string representation without price"""
        az = AvailabilityZone('eu-central-1c', [])
        
        expected = "eu-central-1c for $None/hr"
        self.assertEqual(repr(az), expected)

    def test_repr_string_format(self):
        """Test that repr works correctly when used in string formatting"""
        price_history = [{'SpotPrice': '0.05'}]
        az = AvailabilityZone('us-east-1a', price_history)
        
        result = "Best AZ: {}".format(az)
        expected = "Best AZ: us-east-1a for $0.05/hr"
        self.assertEqual(result, expected)
