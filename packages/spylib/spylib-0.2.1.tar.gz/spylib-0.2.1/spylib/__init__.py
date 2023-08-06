"""A library to facilitate interfacing with Shopify's API"""

__version__ = '0.2.1'


from .store import Store, UniqueStore

__all__ = ['Store', 'UniqueStore']
