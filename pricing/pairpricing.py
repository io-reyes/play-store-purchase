import logging
import play_scraper
import unittest

logger = logging.getLogger(__name__)

class PairPricing:
    def __init__(self, free, paid):
        self.free = free
        self.paid = paid

        self.free_details = PairPricing._scrape_play_store(self.free)
        self.paid_details = PairPricing._scrape_play_store(self.paid)

    def is_available(self):
        return self.free_details is not None and self.paid_details is not None

    def get_price(self):
        if(self.paid_details is not None):
            price_str = self.paid_details['price']
            price = float(price_str.replace('$', '', 1))
            logger.info('%s costs %f' % (self.paid, price))
            return price

        else:
            logger.warning('Paid app %s is not available' % self.paid)
            return -1.00

    def __str__(self):
        if(self.is_available()):
            return '%s,%s,%f' % (self.free, self.paid, self.get_price())
        else:
            return '%s,%s,UNAVAILABLE' % (self.free, self.paid)

    @staticmethod
    def _scrape_play_store(app):
        try:
            details = play_scraper.details(app)
            logger.info('Found Play Store data for %s' % app)
            return details
        except Exception as e:
            logger.warning('Exception while scraping for %s' % app)
            return None

class PairPricingTest(unittest.TestCase):
    def test_valid_pair(self):
        free = 'air.com.rotorzone.balancelite'
        paid = 'air.com.rotorzone.rotorbalance'
        pair = PairPricing(free, paid)

        self.assertTrue(pair.is_available())
        self.assertEqual(pair.get_price(), 2.99)

    def test_missing_free(self):
        free = 'fake.app.aaabbcc982389'
        paid = 'air.com.rotorzone.rotorbalance'
        pair = PairPricing(free, paid)

        self.assertFalse(pair.is_available())
        self.assertEqual(pair.get_price(), 2.99)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
