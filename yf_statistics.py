import yfinance as yf
from datetime import date, datetime
from psycopg2 import sql, DatabaseError, extras
from yahoofinance import get_stock_data
import pandas as pd
import json
from util import db_connection, date_only
from datetime import datetime
import logging


def is_statistics_exist(conn, symbol, one_date):
    try:
        """ read from support_resistance table """
        cur = conn.cursor()

        query = """SELECT symbol FROM statistics where symbol=%s and published_on >= %s"""
        # execute the SELECT statement
        cur.execute(query, (symbol, one_date,))
        # get the generated id back
        result = cur.fetchone()
        conn.commit()
        if (result == None):
            return False
        else:
            return True
    except (Exception, DatabaseError) as error:
        print(error)
        return False


def create_statistic(conn, symbol, one_date):
    try:
        cur = conn.cursor()
        query = """INSERT INTO statistics (symbol, published_on)
                VALUES(%s, %s) RETURNING id;"""
        id = None
        # execute the INSERT statement
        cur.execute(query, (symbol, one_date,))
        # get the generated id back
        id = cur.fetchone()[0]
        conn.commit()
        return id
    except (Exception, DatabaseError) as error:
        print(error)
        return False


def add_statistic(conn, symbol, one_date, key, value):
    try:
        cur = conn.cursor()
        query = """UPDATE statistics SET
                    {} = true,
                    {} = %s
                WHERE symbol=%s AND published_on=%s
        """
        id = None
        # execute the UPDATE statement
        data = ""
        if isinstance(value, pd.DataFrame):
            data = value.to_json(orient="split")
        elif isinstance(value, pd.Series):
            data = value.to_json(orient="split")
        else:
            data = json.dumps(value, indent=4)
        boolean_column = "b_" + key
        column = key
        cur.execute(
            sql.SQL(query).format(sql.Identifier(
                boolean_column), sql.Identifier(column)),
            [data, symbol, one_date])
        # cur.execute(sql, ("b_" + key, symbol, one_date,))
        # get the generated id back
        conn.commit()
        return True
    except (Exception, DatabaseError) as error:
        print(error)
        return False


def add_vitals(conn, symbol, one_date, info, institutional_holders):
    try:
        cur = conn.cursor()
        query = """INSERT INTO Vitals
                    (symbol, sector, summary,
                    average_volume_10days, short_volume, name,
                    short_percent, float_volume, industry,
                    major_investor, published_on)
                    VALUES (%s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s)
                    ON CONFLICT(symbol)
                    DO
                    UPDATE SET
                        sector = EXCLUDED.sector,
                        summary = EXCLUDED.summary,
                        average_volume_10days = EXCLUDED.average_volume_10days,
                        short_volume = EXCLUDED.short_volume,
                        name = EXCLUDED.name,
                        short_percent = EXCLUDED.short_percent,
                        float_volume = EXCLUDED.float_volume,
                        industry = EXCLUDED.industry,
                        major_investor = EXCLUDED.major_investor,
                        published_on = EXCLUDED.published_on
        """
        # execute the UPDATE statement
        sector = info['sector']
        summary = info['longBusinessSummary']
        avg_vol_10days = info['averageVolume10days']
        short_volume = info['sharesShort']
        name = info['shortName']
        short_percent = info['shortRatio']
        float_volume = info['floatShares']
        industry = info['industry']
        institutions = 0
        if isinstance(institutional_holders, pd.DataFrame):
            institutions = institutional_holders.shape[0]
        cur.execute(query, (symbol, sector, summary,
                            avg_vol_10days, short_volume, name,
                            short_percent, float_volume, industry,
                            institutions, one_date,))
        # cur.execute(sql, ("b_" + key, symbol, one_date,))
        # get the generated id back
        conn.commit()
        return True
    except (Exception, DatabaseError) as error:
        print(error)
        return False


def yf_save_stastics(conn, symbol, one_date):
    msft = yf.Ticker(symbol)

    # get stock info
    data = msft.info
    add_statistic(conn, symbol, one_date, "info", data)

    # show institutional holders
    institutional_holders = msft.institutional_holders
    add_statistic(conn, symbol, one_date,
                  "institutional_holders", institutional_holders)

    add_vitals(conn, symbol, one_date, data, institutional_holders)

    try:
        # show actions (dividends, splits)
        actions = msft.actions
        add_statistic(conn, symbol, one_date, "actions", actions)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show dividends
        dividends = msft.dividends
        add_statistic(conn, symbol, one_date, "dividends", dividends)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show splits
        splits = msft.splits
        add_statistic(conn, symbol, one_date, "splits", splits)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show financials
        financials = msft.financials
        add_statistic(conn, symbol, one_date, "financials", financials)
        quarterly_financials = msft.quarterly_financials
        add_statistic(conn, symbol, one_date,
                      "quarterly_financials", quarterly_financials)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show major holders
        major_holders = msft.major_holders
        add_statistic(conn, symbol, one_date, "major_holders", major_holders)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show balance sheet
        balance_sheet = msft.balance_sheet
        add_statistic(conn, symbol, one_date,
                      "balance_sheet", balance_sheet)
        quarterly_balance_sheet = msft.quarterly_balance_sheet
        add_statistic(conn, symbol, one_date,
                      "quarterly_balance_sheet", quarterly_balance_sheet)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show cashflow
        cashflow = msft.cashflow
        add_statistic(conn, symbol, one_date, "cashflow", cashflow)
        quarterly_cashflow = msft.quarterly_cashflow
        add_statistic(conn, symbol, one_date,
                      "quarterly_cashflow", quarterly_cashflow)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show earnings
        earnings = msft.earnings
        add_statistic(conn, symbol, one_date, "earnings", earnings)
        quarterly_earnings = msft.quarterly_earnings
        add_statistic(conn, symbol, one_date,
                      "quarterly_earnings", quarterly_earnings)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show sustainability
        sustainability = msft.sustainability
        add_statistic(conn, symbol, one_date, "sustainability", sustainability)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show analysts recommendations
        recommendations = msft.recommendations
        add_statistic(conn, symbol, one_date,
                      "recommendations", recommendations)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show next event (earnings, etc)
        calendar = msft.calendar
        add_statistic(conn, symbol, one_date, "calendar", calendar)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    try:
        # show options expirations
        options = msft.options
        add_statistic(conn, symbol, one_date, "options", options)
    except (Exception, DatabaseError) as error:
        logging.exception()
        print(error)

    # fix it later.  option_chain is a list of DataFrame.  Need to represent them as json.
    # # get option chain for specific expiration
    # option_chain = msft.option_chain()
    # add_statistic(conn, symbol, one_date, "option_chain", option_chain)
    # # data available via: opt.calls, opt.puts


def yf_statistics(symbol, one_date):
    conn = None
    try:
        conn = db_connection()
        current_date = date_only(one_date)
        yf_save_stastics(conn, symbol, current_date)
        print('statistics saved')
    except (Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def get_vitals(symbol, current_date):
    conn = None
    try:
        one_date = date_only(current_date)
        conn = db_connection()
        """ read from support_resistance table """
        cur = conn.cursor(cursor_factory=extras.DictCursor)

        query = """SELECT ROW_TO_JSON(a) FROM (SELECT * FROM vitals where symbol=%s) a"""
        # execute the SELECT statement
        cur.execute(query, (symbol,))
        # get the generated id back
        result = cur.fetchone()
        conn.commit()
        if result == None or result[0]['published_on'] != one_date.strftime("%Y-%m-%d"):
            return False, {}
        else:
            return True, result
    except (Exception, DatabaseError) as error:
        print(error)
        return False, {}
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def yf_vitals(symbol, one_date):
    issuccess, vitals = get_vitals(symbol, one_date)
    if (issuccess):
        return vitals
    else:
        yf_statistics(symbol, one_date)
        issuccess, vitals = get_vitals(symbol, one_date)
        return vitals if issuccess else {}


if __name__ == '__main__':
    result = yf_vitals('BTX', datetime.today())
    print(result)
