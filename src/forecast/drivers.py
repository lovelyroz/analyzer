from typing import Optional
from src.forecast.schema import SingleForecastChain

class ForecastDriver:

    @staticmethod
    def build_general_chain(
        base_revenue: float,
        growth_rate: float,
        operating_margin: float,
        net_margin: float,
        share_count: float
    ) -> SingleForecastChain:
        """
        ساخت زنجیره پیش‌بینی برای صنایع غیرمالی (عمومی):
        Revenue -> Operating Profit -> Net Profit -> EPS
        """
        if share_count <= 0:
            return SingleForecastChain(None, None, None, None)

        forecast_revenue = base_revenue * (1.0 + growth_rate)
        forecast_op_profit = forecast_revenue * (operating_margin / 100.0)
        forecast_net_profit = forecast_revenue * (net_margin / 100.0)
        forecast_eps = forecast_net_profit / share_count

        return SingleForecastChain(
            revenue=round(forecast_revenue, 2),
            operating_profit=round(forecast_op_profit, 2),
            net_profit=round(forecast_net_profit, 2),
            eps=round(forecast_eps, 2)
        )

    @staticmethod
    def build_holding_chain(
        base_net_profit: float,
        nav_growth_rate: float,
        share_count: float
    ) -> SingleForecastChain:
        """
        ساخت زنجیره پیش‌بینی برای هلدینگ‌ها (سود خالص وابسته به رشد NAV)
        P/NAV در Stage 7 محاسبه خواهد شد و در اینجا وارد نمی‌شود.
        """
        if share_count <= 0:
            return SingleForecastChain(None, None, None, None)

        forecast_net_profit = base_net_profit * (1.0 + nav_growth_rate)
        forecast_eps = forecast_net_profit / share_count

        return SingleForecastChain(
            revenue=None,
            operating_profit=None,
            net_profit=round(forecast_net_profit, 2),
            eps=round(forecast_eps, 2)
        )