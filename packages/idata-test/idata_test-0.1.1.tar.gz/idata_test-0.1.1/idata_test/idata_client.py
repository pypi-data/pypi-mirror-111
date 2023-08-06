import requests as r

from pprint import pprint
from colorama import Fore, Style
from typing import Optional, Union


def color_print(text):
    print(Fore.RED + "[WARNING] " + text + Style.RESET_ALL)


def help_manager(func):
    def wrapper(self, *args, **kwargs):
        if len(args) > 0 and args[0] == "?":
            print(func.__doc__)
            return
        return func(self, *args, **kwargs)
    return wrapper


def session_manager(func):
    RENEW_LIMIT = 1000 * 1000 # max. 1800 * 1000 milliseconds or  30 minutes

    def wrapper(self, *args, **kwargs):
        if self.session_token is None:
            self.get_session_token()

        valid_for = self.session_token_expires_in()
        if valid_for < RENEW_LIMIT:
            self.renew_session_token()
        elif valid_for is None:
            self.get_session_token()

        retval = func(self, *args, **kwargs)
        print()
        return retval
    return wrapper


class IData:
    """
    Python interface for http://api.idatamedia.org
    """
    API_URL = "http://api.idatamedia.org/"

    def __init__(self, api_key=None, session_token=None, verbose=False, raw=False):
        self.API_KEY = api_key
        self.verbose = verbose
        self.raw = raw
        self.session_token = session_token

    def __print_response(self, resp):
        """

        :param obj:
        :return:
        """
        if self.raw is True:
            pprint(resp)

    @help_manager
    def __m(self, text):
        """
        This function to be called when verbose is True
        :param text: Verbose message
        :return: None
        """
        if self.verbose is True:
            print(Fore.CYAN + "[INFO] " + text + Style.RESET_ALL)

    @help_manager
    def api_call(self, extension="", payload=None):
        """

        :param extension:
        :param payload:
        :return:
        """
        try:
            resp = r.get(self.API_URL + extension, params=payload)
            self.__m(f"API call to: {resp.url}")
            resp = resp.json()

            self.__print_response(resp)

            errors = resp.get("Errors", None)

            if errors:
                for error in errors:
                    error_status = error.get("Status", None)
                    error_detail = error.get("Details", None)

                    color_print(f"Error {error_status}: {error_detail}")

                    # if error_status == 401:
                    #     exit()

            retval = resp.get("Result", None)

            if retval is None:
                return {}
            return retval

        except Exception as e:
            color_print(f"Unexpected Error: {e}")
            return {}

    @help_manager
    def set_api_key(self, API_KEY):
        """
        Register your API key to be able to get a session token.
        """
        if API_KEY:
            self.API_KEY = API_KEY
            self.__m(f"Stored the new API key {self.API_KEY}")
        else:
            self.__m(f"You must provide a valid API key.")

        return None

    @help_manager
    def print_api_key(self):
        """
        Return the API key that was set with the set_api_key command.
        """
        return self.API_KEY

    @help_manager
    def get_api_address(self):
        """
        Returns the API address
        """
        return self.API_URL

    @help_manager
    def get_api_version(self):
        """
        Returns the API version number
        """
        resp = self.api_call("GetAPIVersion")
        return resp.get("Version")


    @help_manager
    def get_session_token(self):
        """

        [*] https://www.idatamedia.org/api-docs#sessiontoken

        :return:
        """

        payload = {
            "APIKey": self.API_KEY,
        }

        self.__m(f"Retrieving session token using: {self.API_KEY}")
        resp = self.api_call("GetSessionToken", payload)
        session_token = resp.get("SessionToken", None)
        self.__m(f"Session token retrieved: {session_token}")

        self.session_token = session_token

        return session_token

    @help_manager
    def session_token_expires_in(self):
        """
        Session tokens expire in 30 minutes.

        [*] https://www.idatamedia.org/api-docs#querysessiontoken

        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        self.__m(f"Retrieving expiration time for {self.session_token}")
        resp = self.api_call("SessionTokenExpires", payload)
        remaining = resp.get('Remaining', None)
        self.__m(f"Remaining {remaining} ms.")

        return remaining

    @help_manager
    def renew_session_token(self):
        """
        Extends expiration of session_token

        [*] https://www.idatamedia.org/api-docs#renewsessiontoken
        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        self.__m(f"Renewing session token.")
        resp = self.api_call("RenewSessionToken", payload)
        self.__m(f"Session token renewed.")

        return resp

    @help_manager
    def revoke_session_token(self):
        """

        [*] https://www.idatamedia.org/api-docs#revokesessiontoken

        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }
        self.__m(f"Revoking following session token: {self.session_token}")
        resp = self.api_call("RevokeSessionToken", payload)
        resp_details = resp.get("Details", None)
        self.__m(f"{resp_details}.")

        return resp_details

    @session_manager
    @help_manager
    def get_datasource(self,
                       datasource: str,
                       datatree: Optional[bool] = None,
                       category_list: Optional[bool] = None,
                       user_category_list: Optional[bool] = None) -> dict:
        """
        This API call no longer works!

        [*] https://www.idatamedia.org/api-docs#getonedatasource

        :param datasource:
        :param datatree: Default: True
        :param category_list: Default: True
        :param user_category_list: Default: True
        :return:
        """
        payload = {
            "SessionToken": self.session_token,
            "Datasource": datasource,
            "ReturnDataTree": None if datatree is None else str(datatree).lower(),
            "ReturnCategoryList": None if datasource is None else str(datasource).lower(),
            "ReturnUserCategoryList": None if user_category_list is None else str(user_category_list).lower(),
        }

        color_print("THIS API CALL HAS BEEN DEPRECIATED!")

        self.__m(f"Retreiving datasource for {datasource}")
        resp = self.api_call("GetDatasource", payload)
        resp_details = resp.get("Details", None)
        self.__m("Datasource retrieved.")

        return resp_details

    @session_manager
    @help_manager
    def get_all_datasources(self,
                            category_list: Optional[bool] = None,
                            datatree: Optional[bool] = None,
                            user_access: Optional[bool] = None) -> list:
        """

        [*] https://www.idatamedia.org/api-docs#getalldatasource

        :param category_list: Default: True
        :param datatree: Default: True. Doesn't work as of now
        :param user_category_list: Default: True. doesn't work as of now
        :return:
        """
        payload = {
            "SessionToken":             self.session_token,
            "ReturnCategoryList":       None if category_list is None else str(category_list).lower(),
            # "ReturnDataTree":         None if datatree is None else str(datatree).lower(),
            # "ReturnUserAccess":       None if user_access is None else str(user_access).lower(),
        }
        self.__m(f"Retreiving all datasources...")
        resp = self.api_call("GetAllDatasources", payload)
        self.__m(f"Total {len(resp)} datasources retrieved.")

        return resp

    @session_manager
    @help_manager
    def get_user_datasources(self,
                             category_list: Optional[bool] = None,
                             datatree: Optional[bool] = None) -> list:
        """

        [*] https://www.idatamedia.org/api-docs#userdatasource

        :param category_list: Default: True.
        :param datatree: Default: False. Doesn't work as of now
        :return:
        """
        payload = {
            "SessionToken": self.session_token,
            "ReturnCategoryList": None if category_list is None else str(category_list).lower(),
            # "ReturnDataTree":       None if datatree is None else str(datatree).lower(),
        }
        self.__m("Retrieving user datasources.")
        resp = self.api_call("GetUserDatasources", payload)
        self.__m(f"Total {len(resp)} user datasources retrieved.")

        return resp

    @session_manager
    @help_manager
    def get_dataset_of(self,
                       datasource: str,
                       filters: Optional[str] = None,
                       case_sensitive: Optional[bool] = None,
                       sort_order: Optional[str] = None,
                       sort_columns: Optional[str] = None,
                       ignore_empty: Optional[bool] = None,
                       short_record: Optional[bool] = None,
                       category_tree: Optional[bool] = None,
                       category_list: Optional[bool] = None,
                       user_category_list: Optional[bool] = None,
                       category_filter: Optional[str] = None,
                       page: Optional[int] = None,
                       rows: Optional[int] = None,
                       values_since: Optional[str] = None) -> dict:
        """
        Retrieve the metadata for all (or some) of the datasets in one datasource.

        [*] https://www.idatamedia.org/api-docs#datasetsonesource

        :param datasource:
        :param filters: Default: None
        :param case_sensitive: Default: False
        :param sort_order: Default: "asc". "asc" for ascending and "desc" for descending
        :param sort_columns: Default: "Symbol"
        :param ignore_empty: Default: False
        :param short_record: Default: True
        :param category_tree: Default: False
        :param category_list: Default: False
        :param user_category_list: Default: False
        :param category_filter: Default: None
        :param page: Default: 1
        :param rows: Default: 100. Max. 5000
        :param values_since: Default: "Earliest". "YYYY-MM-DD" format or "Earliest"
        :return:
        """

        payload = {
            "SessionToken":             self.session_token,
            "Datasource":               datasource,
            "Filter":                   filters,
            "CaseSensitive":            None if case_sensitive is None else str(case_sensitive).lower(),
            "SortOrder":                sort_order,
            "SortColumns":              sort_columns,
            "IgnoreEmpty":              None if ignore_empty is None else str(ignore_empty).lower(),
            "ShortRecord":              None if short_record is None else str(short_record).lower(),
            "ReturnCategoryTree":       None if category_tree is None else str(category_tree).lower(),
            "ReturnCategoryList":       None if category_list is None else str(category_list).lower(),
            "ReturnUserCategoryList":   None if user_category_list is None else str(user_category_list).lower(),
            "CategoryFilter":           category_filter,
            "Page":                     page,
            "Rows":                     rows,
            "ValuesSince":              values_since,
        }
        self.__m(f"Retrieving datasets for {datasource}.")
        resp = self.api_call("GetDatasets", payload)
        self.__m("Datasets retrieved.")

        return resp

    @session_manager
    @help_manager
    def get_datasets(self,
                     symbols: list,
                     short_record: Optional[bool] = None) -> dict:
        """

        [*] https://www.idatamedia.org/api-docs#datasetsmultiplesources

        :param symbols: A list of symbols exmp: datasource/symbol
        :param short_record: Default: False. Doesn't work as of now.
        :return:
        """

        payload = {
            "SessionToken":     self.session_token,
            "Symbols[]":        symbols,
            "ShortRecord":      None if short_record is None else str(short_record).lower(),
        }

        self.__m(f"Retrieving selected datasets: {', '.join(symbols)}")
        resp = self.api_call("GetSelectedDatasets", payload)

        if resp:
            self.__m("Selected datasets retrieved.")

        return resp

    @session_manager
    @help_manager
    def get_favorites_status(self):
        """

        [*] https://www.idatamedia.org/api-docs#favoritestatus

        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        resp = self.api_call("GetFavoritesStatus", payload)

        return resp

    @session_manager
    @help_manager
    def get_favorites(self,
                      ignore_empty: bool = False,
                      page: int = 1,
                      rows: int = 50,
                      data_category: Optional[str] = None,
                      returntree: Optional[bool] = None) -> dict:
        """

        [*] https://www.idatamedia.org/api-docs#favoritesmetadata


        :param ignore_empty: Default: False
        :param page: Default: 1
        :param rows: Default:50, Max. 500
        :param data_category: Doesn't work as of now. Format: datasource/category-1
        :param returntree: Default: True
        :return:
        """
        payload = {
            "SessionToken":     self.session_token,
            "IgnoreEmpty":      str(ignore_empty).lower(),
            "Page":             page,
            "Rows":             rows,
            "DataCategory":     data_category,
            "ReturnTree":       None if returntree is None else str(returntree).lower(),
        }

        self.__m("Retrieving user favorites.")
        resp = self.api_call("GetUserFavorites", payload)

        if resp:
            self.__m("User favorites retrieved.")

        return resp

    @session_manager
    @help_manager
    def add_favorites(self,
                      series: list):
        """

        [*] https://www.idatamedia.org/api-docs#adddatasetstofavorites

        :param series: A list of  datasource/symbol
        :return:
        """

        payload = {
            "SessionToken": self.session_token,
            "Series[]":     series,
        }

        self.__m(f"Adding {', '.join(series)} to favorites.")
        resp = self.api_call("AddFavorites", payload)

        status_code = resp.get("Status", None)
        detail = resp.get("Detail", None)

        if status_code == 204:
            self.__m("This symbol is already in  the User Favorites. Request ignored.")
        elif status_code == 200:
            self.__m("A new symbol was successfully added.")
        else:
            self.__m(f"Unknown status code: {status_code}, {detail}")

        return resp

    @session_manager
    @help_manager
    def del_favorites(self,
                      series: list) -> dict:
        """

        [*] https://www.idatamedia.org/api-docs#removedatasetfromfavorites

        :param series:
        :return:
        """

        payload = {
            "SessionToken": self.session_token,
            "Series[]":     series,
        }

        self.__m(f"Removing {', '.join(series)} from favorites.")
        resp = self.api_call("RemoveFavorites", payload)

        status_code = resp.get("Status", None)
        detail = resp.get("Detail", None)

        if status_code == 204:
            self.__m("This symbol is not in the User Favorites. Request ignored.")
        elif status_code == 200:
            self.__m("New symbol successfully deleted.")
        else:
            self.__m(f"Unknown status code: {status_code}, {detail}")

        return resp

    @session_manager
    @help_manager
    def get_dataset_values(self,
                           series: list,
                           rc: bool = False,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           periods: Optional[int] = None,
                           common_start: Optional[bool] = None,
                           common_end: Optional[bool] = None,
                           date_format: Optional[str] = None,
                           prefill: Optional[bool] = None,
                           handle_weekends: Optional[str] = None,
                           freq: Optional[str] = None,
                           fill: Optional[bool] = None,
                           sparse: Optional[str] = None,
                           sparse_na: Optional[bool] = None,
                           use_period_start_date: Optional[bool] = None,
                           freq_start_date: Optional[int] = None,
                           freq_end_date: Optional[int] = None,
                           freq_start_date2: Optional[int] = None,
                           freq_end_date2: Optional[int] = None,
                           weekends_in_avg_result: Optional[str] = None,
                           rounding: Optional[Union[int, str]] = None) -> list:
        """

        [*] https://www.idatamedia.org/api-docs#getdatasetvalues
        [*] https://www.idatamedia.org/api-docs#getdatasetvaluesrc

        :param series:
        :param rc: formatted row by column
        :param start_date: Default: "Earliest"
        :param end_date: Default: "Latest"
        :param periods: Default: None
        :param common_start: Default: False
        :param common_end: Default: False
        :param date_format: Default: "YYYY-MM-DD"
        :param prefill: Default: False
        :param handle_weekends: Default: "Def"
        :param freq: Default: "d"
        :param fill: Default: False
        :param sparse: Default: "leadtrail"
        :param sparse_na: Default: True
        :param use_period_start_date: Default: False
        :param freq_start_date: Default: 1
        :param freq_end_date: Default: 31
        :param freq_start_date2: Default: 16
        :param freq_end_date2: Default: 31
        :param weekends_in_avg_result: "def"
        :param rounding: Default: "def"
        :return:
        """

        payload = {
            "SessionToken":         self.session_token,
            "Series[]":             series,
            "StartDate":            start_date,
            "EndDate":              end_date,
            "Periods":              periods,
            "CommonStart":          None if common_start is None else str(common_start).lower(),
            "CommonEnd":            None if common_end is None else str(common_end).lower(),
            "DateFormat":           date_format,
            "Prefill":              None if prefill is None else str(prefill).lower(),
            "HandleWeekends":       handle_weekends,
            "Frequency":            freq,
            "Fill":                 None if fill is None else str(fill).lower(),
            "Sparse":               sparse,
            "SparseNA":             None if sparse_na is None else str(sparse_na).lower(),
            "UsePeriodStartDate":   None if use_period_start_date is None else str(use_period_start_date).lower(),
            "FrequencyStartDay":    freq_start_date,
            "FrequencyEndDay":      freq_end_date,
            "FrequencyStartDay2":   freq_start_date2,
            "FrequencyEndDay2":     freq_end_date2,
            "WeekendsinAvgResult":  weekends_in_avg_result,
            "Rounding":             rounding,
        }

        if rc is True:
            resp = self.api_call("GetValues", payload)
        else:
            resp = self.api_call("GetValuesRC", payload)

        return resp

    @session_manager
    @help_manager
    def get_dataset_values_for_date(self,
                                    series: list,
                                    date: str,
                                    return_latest: Optional[bool] = None,
                                    return_corrections: Optional[bool] = None,
                                    sparks_count: Optional[int] = None,
                                    date_format: Optional[str] = None,
                                    prefill: Optional[bool] = None,
                                    handle_weekends: Optional[str] = None,
                                    freq: Optional[str] = None,
                                    fill: Optional[bool] = None,
                                    use_period_start_date: Optional[bool] = None,
                                    freq_start_date: Optional[int] = None,
                                    freq_end_date: Optional[int] = None,
                                    freq_start_date2: Optional[int] = None,
                                    freq_end_date2: Optional[int] = None,
                                    weekends_in_avg_result: Optional[str] = None,
                                    rounding: Optional[Union[int, str]] = None) -> list:
        """

        [*] https://www.idatamedia.org/api-docs#getdatasetvaluesforadate

        :param series:
        :param date:
        :param return_latest: Default: False
        :param return_corrections: Default: True
        :param sparks_count: Default: 0
        :param date_format: Default: "YYYY-MM-DD"
        :param prefill: Default: False
        :param handle_weekends: Default: "def"
        :param freq: Default: "d"
        :param fill: Default: False
        :param use_period_start_date: Default: False
        :param freq_start_date: Default: 1
        :param freq_end_date: Default: 31
        :param freq_start_date2: Default: 16
        :param freq_end_date2: Default: 31
        :param weekends_in_avg_result: Default: "def"
        :param rounding: Default: "def"
        :return:
        """

        payload = {
            "SessionToken":         self.session_token,
            "Series[]":             series,
            "Date":                 date,
            "ReturnLatest":         None if return_latest is None else str(return_latest).lower(),
            "ReturnCorrections":    None if return_corrections is None else str(return_corrections).lower(),
            "SparksCount":          sparks_count,
            "DateFormat":           date_format,
            "Prefill":              None if prefill is None else str(prefill).lower(),
            "HandleWeekends":       handle_weekends,
            "Frequency":            freq,
            "Fill":                 None if fill is None else str(fill).lower(),
            "UsePeriodStartDate":   None if use_period_start_date is None else str(use_period_start_date).lower(),
            "FrequencyStartDay":    freq_start_date,
            "FrequencyEndDay":      freq_end_date,
            "FrequencyStartDay2":   freq_start_date2,
            "FrequencyEndDay2":     freq_end_date2,
            "WeekendsinAvgResult":  weekends_in_avg_result,
            "Rounding":             rounding,
        }

        resp = self.api_call("GetValuesForDate", payload)

        return resp

    @session_manager
    @help_manager
    def get_account_details(self):
        """

        [*] https://www.idatamedia.org/api-docs#getmyaccountdetails
        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        self.__m("Retrieving account details.")
        resp = self.api_call("GetAccountDetails", payload)
        self.__m("Account details retrieved.")

        return resp

    @session_manager
    @help_manager
    def request_new_api_key(self):
        """
        Return a new API key (the current one will be invalidated!).
        [*] https://www.idatamedia.org/api-docs#newapikey
        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        self.__m("Requesting new API Key...")
        resp = self.api_call("RequestNewAPIKey", payload)
        new_api_key = resp.get("APIkey", None)

        if new_api_key is not None:
            self.__m(f"New API Key returned. {new_api_key}.")
            self.API_KEY = new_api_key
            self.__m("New API Key was reset to default")
            return new_api_key

        self.__m("Failed to retrieve the new API Key.")
        return None

    @session_manager
    @help_manager
    def reset_password(self):
        """

        [*] https://www.idatamedia.org/api-docs#newapikeyemail

        :return:
        """
        payload = {
            "SessionToken": self.session_token,
        }

        self.__m("Resetting password...")
        resp = self.api_call("SendPasswordReset", payload)
        status_code = resp.get("Status", None)
        detail = resp.get("Detail", None)

        if status_code == 200:
            self.__m(f"Password reset successful. {detail}")
        else:
            self.__m(f"Password reset failed. {detail}")
        return detail
