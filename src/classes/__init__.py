import lazy_loader


__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules={
        'Bench',
        'Board',
        'Pool',
        'Shop',
        'Unit',
        'test',
        'util',
    },
    submod_attrs={
        'Pool': [
            'Pool',
        ],
        'Shop': [
            'Shop',
        ],
        'Unit': [
            'Unit',
        ],
        'test': [
            'TestPool',
            'TestShop',
            'TestUnit',
        ],
        'util': [
            'load_shop_odds',
            'load_units',
            'number_shops',
        ],
    },
)

__all__ = ['Bench', 'Board', 'Pool', 'Shop', 'TestPool', 'TestShop',
           'TestUnit', 'Unit', 'load_shop_odds', 'load_units', 'number_shops',
           'test', 'util']

