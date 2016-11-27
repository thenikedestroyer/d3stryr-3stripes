import requests
from settings import user_config
from utils import d_, z_, o_, get_random_user_agent

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings()


def get_client_response():
    """
    Gets client-level inventory data.
    """
    headers = {'User-Agent': get_random_user_agent()}
    session = requests.Session()
    session.verify = False
    session.cookies.clear()
    skus = ','.join(['{sku}_{size_id}'.format(sku=user_config.masterPid, size_id=x) for x in range(510, 820, 10)])

    # Other countries will use US format like MX.
    # They can just request US value for parametersLocale in config.cfg
    if user_config.parametersLocale == 'US':
        url = (
            'http://{0}-us-adidasgroup.demandware.net/s/adidas-{1}'
            '/dw/shop/v15_6/products/({2})'
            '?client_id={3}&expand=availability,variations,prices'
        ).format(user_config.apiEnv, user_config.marketLocale, skus, user_config.clientId,)
    else:
        url = (
            'http://{0}-store-adidasgroup.demandware.net/s/adidas-{1}'
            '/dw/shop/v15_6/products/({2})'
            '?client_id={3}&expand=availability,variations,prices'
        ).format(user_config.apiEnv, user_config.marketLocale, skus, user_config.clientId,)
    if user_config.debug:
        print(d_(), z_('Debug'), o_(url))

    return session.get(url=url, headers=headers)


def get_variant_response():
    """
    Gets variant-level inventory data.
    """
    headers = {'User-Agent': get_random_user_agent()}
    session = requests.Session()
    session.verify = False
    session.cookies.clear()

    # Not sure why I even bother making a case for Portugal if dude on twitter
    # keeps telling it doesnt work. Da fuq is MLT?
    if user_config.market == 'PT':
        url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-'
            '{1}-Site/MLT/Product-GetVariants?pid={2}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.masterPid,)
    else:
        url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-'
            '{1}-Site/{2}/Product-GetVariants?pid={3}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.market, user_config.masterPid,)

    if user_config.debug:
        print(d_(), z_('Debug'), o_(variantStockURL))

    return session.get(url=url, headers=headers)
