# Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

from dateutil.relativedelta import relativedelta
from flask import flash, redirect, render_template, session
from functools import wraps

from models import MonthlyWeights


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def weight_change(patient_id, interval_months, current_weight, weight_date):
    """Calculates percentage weight change in a given interval of months"""
    # Calculate the date interval_months ago from weight_date
    interval_ago = weight_date - relativedelta(months=interval_months)

    # Query database to find weight record at the closest date before the calculated date
    weight_at_interval_ago = (
        MonthlyWeights.query.filter_by(patient_id=patient_id)
        .filter(MonthlyWeights.weight_date <= interval_ago)
        .order_by(MonthlyWeights.weight_date.desc())
        .first()
    )

    if weight_at_interval_ago is None:
        # If no weight record is found at interval, attempt to find weights one month before and one month after interval
        interval_ago_before = interval_ago - relativedelta(months=1)
        weight_before = (
            MonthlyWeights.query.filter(
                MonthlyWeights.patient_id == patient_id,
                MonthlyWeights.weight_date == interval_ago_before,
            )
            .order_by(MonthlyWeights.weight_date.desc())
            .first()
        )

        interval_ago_after = interval_ago + relativedelta(months=1)
        weight_after = (
            MonthlyWeights.query.filter(
                MonthlyWeights.patient_id == patient_id,
                MonthlyWeights.weight_date == interval_ago_after,
            )
            .order_by(MonthlyWeights.weight_date.asc())
            .first()
        )

        if weight_before and weight_after:
            # If both neighboring weights are available, calculate the average weight to estimate the change
            interval_average_weight = (
                weight_before.patient_weight + weight_after.patient_weight
            ) / 2

            # Calculate the percent change using the average weight
            percent_change = (
                (current_weight.patient_weight - interval_average_weight)
                / interval_average_weight
            ) * 100

            flash(
                f"No weight found for given interval. Average of weights from surrounding months: {interval_average_weight:.2f}"
            )
            return percent_change
        else:
            # If no neighboring weights available, indicate that there is no data to calculate weight change
            interval_text = (
                f"{interval_months} month{'s' if interval_months > 1 else ''}"
            )
            flash(
                f"No weight found for given interval {interval_text} and no surrounding weights available to calculate average at {weight_date}."
            )
            return 0.0

    # If a weight record is found at the interval, calculate the percent change using the provided current weight
    else:
        percent_change = (
            (current_weight.patient_weight - weight_at_interval_ago.patient_weight)
            / weight_at_interval_ago.patient_weight
        ) * 100

    return percent_change
