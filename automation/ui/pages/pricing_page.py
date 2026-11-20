from .base_page import BasePage

PLANS = ("Solo", "Academy", "Pro", "Enterprise")


class PricingPage(BasePage):
    path = "/pricing"
