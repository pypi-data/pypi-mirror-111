import time

import pandas
from django.conf import settings as conf_settings
from datetime import datetime
import logging

from django_q.models import Task
from django_q import models as q_models
from . import config
import err
from .models import DownloadDeatilsModel
from .services import Services
from . import views
from clickhouse_pool import ChPool

static_root = conf_settings.STATIC_ROOT
media_root = conf_settings.MEDIA_ROOT

# Get an instance of logger
logger_1 = logging.getLogger('django_1')


def fetch_data_and_csv_generation(details):
    """
    status is updated as in progress once the async task get started.
    :param details:
    :return: status or csv_file_name(in case of getting the report data)
    """

    try:
        started_task = Task.objects.all().count()
        succesful_task = q_models.Success.objects.all().count()
        failed_task = q_models.Failure.objects.all().count()
        # Get an instance of ReportStatusView
        report_status = views.ReportStatusView()
        # Get an instance of ReportGenerationView
        report_generation = ReportGenerationView()
        download_obj = DownloadDeatilsModel.objects.get(pk=int(details[0]))
        download_obj.status = "in progress"
        download_obj.download_link = ""
        download_obj.save()
        # set the site_id as None once we select all the sites like india
        if details[8] == 'true':
            [report_data, report_error] = report_generation.find_rtu_data(from_date=details[3], to_date=details[4],
                                                                          report_name=details[1])

        else:
            [report_data, report_error] = report_generation.find_rtu_data(from_date=details[3], to_date=details[4],
                                                                          site_id=details[7],
                                                                          report_name=details[1])
        # based on the values of [report_data, report_error], updating the status as "No Data Found","Failed" or
        # "completed"
        if (report_data is None) and (report_error is None):
            download_obj.status = "No Data Found"
            download_obj.download_link = ""
            download_obj.save()
            # return report_error, report_data, "No Data Found"
        elif report_error is not None:
            download_obj.status = "Failed"
            download_obj.download_link = ""
            download_obj.save()
            # return report_error, report_data, "Failed"
        elif (report_data is not None) and (report_error is None):
            # creating csv_file_name with start date and end date
            csv_file_name = "{}/{}.csv".format(media_root, details[1] + "_btwn_" + str(details[3]) + "_and_" + str(
                    details[4]) + "_" + str(details[0]))
            try:
                # creating a csv file from the data frame of report data
                report_data.to_csv(csv_file_name, index=False, header=True)
                err.Tracker.add_to_tracker('df_to_csv_error', None)
            except Exception as e:
                err.Tracker.add_to_tracker('df_to_csv_error', str(e))
            download_link = details[1] + "_btwn_" + str(details[3]) + "_and_" + str(details[4]) + "_" + str(details[0])
            # if everything works fine,then the status will be updated as completed with download_link
            download_obj.status = "completed"
            download_obj.download_link = download_link
            download_obj.save()
            # return report_error, report_data, csv_file_name

        err.Tracker.add_to_tracker('fetch_data_and_csv_generation', str(report_error))
    except Exception as e:
        err.Tracker.add_to_tracker('fetch_data_and_csv_generation', str(e))
    finally:
        started_task = Task.objects.all().count()
        err.Tracker.add_to_tracker('started_task', str(started_task))
        succesful_task = q_models.Success.objects.all().count()
        err.Tracker.add_to_tracker('succesful_task', str(succesful_task))
        failed_task = q_models.Failure.objects.all().count()
        err.Tracker.add_to_tracker('failed_task', str(failed_task))



class ReportGenerationView:

    def __init__(self):
        """
        created clickhouse client connect
        """
        self.pool = ChPool(host=config.host, port=config.port, user=config.username, password=config.password,
                           database=config.db_name, connections_max=10,
                           settings={'use_numpy': True, 'max_threads': 2})
        self.jinja = views.JinjaSqlQueryView()
        self.general_query = "select distinct {{ select_columns[0] | sqlsafe }} {% for dim in select_columns[1:] %}, " \
                             "{{ dim | sqlsafe }}{%- endfor %} from {{table_name | sqlsafe}} " \
                             "{% if from_day and to_day and rtu_reading_id and (from_hour != None) and (to_hour != " \
                             "None) %}where day between {{from_day}} and {{to_day}} and rtu_reading_id in {{" \
                             "rtu_reading_id | inclause}} and toHour(hour) between {{from_hour}} and {{to_hour}} {% " \
                             "endif %}" \
                             "{% if machine_id %}AND machine_id in {{machine_id | inclause}} {% endif %}" \
                             "{% if group_by_columns %}group by {{ group_by_columns[0] | sqlsafe }} {% for dim in " \
                             "group_by_columns[1:] %}, {{ dim | sqlsafe }} {%- endfor %}{% endif %} " \
                             "{% if order_by_columns %}order by {{ order_by_columns[0] | sqlsafe }} {% for dim in " \
                             "order_by_columns[1:] %}, {{ dim | sqlsafe }}{%- endfor %}{% endif %} "

    def find_rtu_data(self, from_date=datetime.now(), to_date=datetime.now(), site_id=None,
                      report_name="Energy Consumption"):
        """
        executing the query for getting the machine_ids and then call the report generation function with this
        machine_id
        :param from_date,
        :param to_date,
        :param site_id,
        :param report_name,
        :return: [report_data,report_error]
        """
        report_error = None
        report_data = None
        logger_1.debug("Site Id-:{}".format(site_id))
        try:
            if site_id is None:
                machine_id = None
            else:
                logger_1.info("Build the query for machine_id")
                query_machine_id = "SELECT distinct node.node_details_id FROM view_camera_tree_details node JOIN " \
                                   "(SELECT id,name,rgt,lft FROM view_camera_tree_details WHERE id IN %s ) " \
                                   "AS parent ON toInt64(node.parent_id)=toInt64(parent.id) WHERE is_camera=4;" \
                                   % site_id
                logger_1.info(
                    "Query for the machine_id from:{} to:{} for the site_id:{}".format(from_date, to_date, site_id))
                logger_1.debug("Query for the machine_id : {}".format(query_machine_id))
                with self.pool.get_client() as client:
                    machines = client.execute(query_machine_id)
                machine_id = []
                for machine in machines:
                    machine_id.append(machine[0])
            if str(report_name) == "Energy consumption":
                [report_data, report_error_msg] = self.energy_report_generator(from_date, to_date, machine_id)
                err.Tracker.add_to_tracker('energy_report_generator_error', str(report_error_msg))
                if report_error_msg is not None:
                    report_error = report_error_msg
                    return [report_data, report_error]
            elif str(report_name) == "DG UPS":
                [report_data, report_error_msg] = self.dg_ups_report_generator(from_date, to_date, machine_id)
                err.Tracker.add_to_tracker('dg_ups_report_generator_error', str(report_error_msg))
                if report_error_msg is not None:
                    report_error = report_error_msg
                    return [report_data, report_error]
            logger_1.info("Generated report data : {}".format(report_data))
            err.Tracker.add_to_tracker('find_rtu_error', None)
        except Exception as e:
            logger_1.error("failed to get the report data :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('find_rtu_error', str(e))
        return [report_data, report_error]

    def dg_ups_report_generator(self, from_date, to_date, machine_id=None):
        # Extract day and time intervals separately
        from_day = from_date.date()  # Start day
        to_day = to_date.date()  # End day
        from_hour = from_date.hour  # Start hour for each day
        to_hour = to_date.hour  # End hour for each day
        # Creating an empty dictionary to store datasets pulled from Clickhouse
        dataset = dict()
        # Creating an empty dataframe to store the results of the report generation query
        report_data = None
        # Creating an error object to store errors we encounter in the report generation process
        report_error = None
        try:
            # Building the query for DG Running Time Readings
            # Currently we are hard-coding the reading_id (49) which is DG Running Hours (in minutes)
            # Need to replace this hard coding later
            logger_1.info("Building the query for energy readings")
            params = {
                "table_name": config.dg_ups_table_name,
                "group_by_columns": config.dg_ups_group_by_columns,
                "order_by_columns": config.dg_ups_order_by_columns,
                "select_columns": config.dg_ups_select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.dg_ups_rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["DG"], DG_err_msg = self.jinja.apply_sql_template(self.general_query, params)
            if DG_err_msg is not None:
                raise Exception(DG_err_msg)
            else:
                logger_1.debug("Query for the DG running hour readings : {}".format(query))
                logger_1.debug("DG running hour readings query result : {}".format(dataset["DG"]))

        except Exception as e:
            logger_1.error("Querying DG running hour readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        try:
            # Building the query for Phase Voltage, Phase Current Currently we are hard-coding the reading_id (663,
            # 664,665) which are the phase_wise Voltage readings (Phase to Neutral) Currently we are hard-coding the
            # reading_id(666,667,668) which are Current readings Need to replace this hard_coding later
            params = {
                "table_name": config.dg_ups_voltage_table_name,
                "group_by_columns": config.dg_ups_voltage_group_by_columns,
                "order_by_columns": config.dg_ups_voltage_order_by_columns,
                "select_columns": config.dg_ups_voltage_select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.dg_ups_voltage_rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["Voltage_Current"], volt_current_err_msg = self.jinja.apply_sql_template(self.general_query,
                                                                                                    params)
            if volt_current_err_msg is not None:
                raise Exception(volt_current_err_msg)
            else:
                logger_1.debug("Query for the Voltage and Current readings : {}".format(query))
                logger_1.debug("Voltage and Current readings query result:-{}".format(dataset["Voltage_Current"]))
        except Exception as e:
            logger_1.error("Querying Voltage and Current Readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        try:
            # Building the query for UPS Battery Voltage Readings
            # Currently we are hard-coding the reading_id (23) which is the UPS Battery Voltage
            # Need to replace this hard_coding later
            params = {
                "table_name": config.dg_ups_battery_table_name,
                "group_by_columns": config.dg_ups_battery_group_by_columns,
                "order_by_columns": config.dg_ups_battery_order_by_columns,
                "select_columns": config.dg_ups_battery_select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.dg_ups_battery_rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["UPS_Battery_Voltage"], ups_battery_vol_err_msg = self.jinja.apply_sql_template(
                self.general_query, params)
            if ups_battery_vol_err_msg is not None:
                raise Exception(ups_battery_vol_err_msg)
            else:
                logger_1.debug("Query for the UPS Battery Voltage readings : {}".format(query))
                logger_1.debug("UPS Battery Voltage readings query result:-{}".format(dataset["UPS_Battery_Voltage"]))
        except Exception as e:
            logger_1.error("Querying UPS Battery Voltage  Readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        try:
            # Building the query for DG Battery Voltage Readings
            # Currently we are hard-coding the reading_id (50) which is the DG Battery Voltage
            # Need to replace this hard_coding later
            params = {
                "table_name": config.dg_battery_voltage_table_name,
                "group_by_columns": config.dg_battery_voltage_group_by_columns,
                "order_by_columns": config.dg_battery_voltage_order_by_columns,
                "select_columns": config.dg_battery_voltage_select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.dg_battery_voltage_rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["DG_Battery_Voltage"], dg_battery_vol_err_mdg = self.jinja.apply_sql_template(
                self.general_query, params)
            if dg_battery_vol_err_mdg is not None:
                raise Exception(dg_battery_vol_err_mdg)
            else:
                logger_1.debug("Query for the DG Battery Voltage readings : {}".format(query))
                logger_1.debug("DG Battery Voltage readings query result:-{}".format(dataset["DG_Battery_Voltage"]))
        except Exception as e:
            logger_1.error("Querying DG Battery Voltage  Readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        try:
            params = {
                "table_name": config.dg_ups_machine_details_table_name,
                "group_by_columns": None,
                "order_by_columns": None,
                "select_columns": config.dg_ups_machine_details_select_columns,
                "from_day": None,
                "to_day": None,
                "rtu_reading_id": None,
                "from_hour": None,
                "to_hour": None,
                "machine_id": None
            }
            query, dataset["machine_details"], machine_details_error_msg = self.jinja.apply_sql_template(
                self.general_query, params)
            if machine_details_error_msg is not None:
                raise Exception(machine_details_error_msg)
            else:
                pass
        except Exception as e:
            logger_1.error("Querying Machine Details has failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        if dataset["DG"].empty or dataset["machine_details"].empty:
            logger_1.info("Empty Data set")
            return [report_data, report_error]

        try:
            # Merging the key columns (machine name, location etc)
            # report_data = report_data.merge(dataset["key_columns"], how="right", left_index=True, right_index=True)
            report_data = dataset["DG"]
            report_data = report_data.merge(dataset["machine_details"], how="left", on="machine_id")
        except Exception as e:
            logger_1.error("Merging the key columns has failed : {}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]

        # Pivot Voltage and Current

        try:
            if not dataset["Voltage_Current"].empty:
                logger_1.info("Transposing voltage and current readings")
                dataset["Voltage_Current"].set_index(['machine_id', 'day'], drop=True, inplace=True)
                report_data_voltage_current = dataset["Voltage_Current"].pivot(columns='rtu_reading_id')
                report_data_voltage_current.columns = [663, 664, 665, 666, 667, 668]

            logger_1.info("Setting index for UPS and DG Battery readings")
            if not dataset["UPS_Battery_Voltage"].empty:
                dataset["UPS_Battery_Voltage"].set_index(['machine_id', 'day'], drop=True, inplace=True)
            if not dataset["DG_Battery_Voltage"].empty:
                dataset["DG_Battery_Voltage"].set_index(['machine_id', 'day'], drop=True, inplace=True)

        except Exception as e:
            print("Transposing Voltage and Current data has failed : {}".format(e))
            logger_1.error("Transposing Voltage and Current data has failed : {}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]  #

        # Set composite index
        try:
            print("Setting composite index on Report Data")
            logger_1.info("Setting composite index on Report Data")
            report_data['date'] = report_data['day']
            report_data.set_index(['machine_id', 'day'], drop=True, inplace=True)
            # Combining data into report
            # Important Note: Is this the best efficiency we can get in merge?
            # TODO: Think of a better optimization to merge
            logger_1.info("Merging Energy Meter data with Voltage and Current data")
            if not dataset["Voltage_Current"].empty:
                report_data = report_data.merge(report_data_voltage_current, how="left", left_index=True,
                                                right_index=True)
            if not dataset["UPS_Battery_Voltage"].empty:
                report_data = report_data.merge(dataset["UPS_Battery_Voltage"], how="left", left_index=True,
                                                right_index=True)
            if not dataset["DG_Battery_Voltage"].empty:
                report_data = report_data.merge(dataset["DG_Battery_Voltage"], how="left", left_index=True,
                                                right_index=True)
        except Exception as e:
            logger_1.error("Indexing and Merging data has failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]  #

        # Replacing missing values (should occur only in current)
        # But we need to verify this carefully, if any zeroes appear other than in current
        # in the final report
        logger_1.info("Filling null values in merged data")
        report_data.fillna(0, inplace=True)

        try:
            report_data["dg_running_duration"] = report_data["dg_running_max"] - report_data["dg_running_min"]
            if not dataset["Voltage_Current"].empty:
                if not dataset["UPS_Battery_Voltage"].empty:
                    if not dataset["DG_Battery_Voltage"].empty:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration', 663,
                             664, 665, 666, 667, 668, 'ups_battery_voltage_min', 'ups_battery_voltage_max',
                             'dg_battery_voltage_min', 'dg_battery_voltage_max']]
                    else:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration', 663,
                             664, 665, 666, 667, 668, 'ups_battery_voltage_min', 'ups_battery_voltage_max']]
                else:
                    if not dataset["DG_Battery_Voltage"].empty:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration', 663,
                             664, 665, 666, 667, 668,
                             'dg_battery_voltage_min', 'dg_battery_voltage_max']]
                    else:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration', 663,
                             664, 665, 666, 667, 668]]

            else:
                if not dataset["UPS_Battery_Voltage"].empty:
                    if not dataset["DG_Battery_Voltage"].empty:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration',
                             'ups_battery_voltage_min', 'ups_battery_voltage_max',
                             'dg_battery_voltage_min', 'dg_battery_voltage_max']]
                    else:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration',
                             'ups_battery_voltage_min', 'ups_battery_voltage_max']]
                else:
                    if not dataset["DG_Battery_Voltage"].empty:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration',
                             'dg_battery_voltage_min', 'dg_battery_voltage_max']]
                    else:
                        report_data = report_data[
                            ['machine_name', 'date', 'dg_running_min', 'dg_running_max', 'dg_running_duration']]

            column_name_map = {'machine_name': 'machine_name',
                               'date': 'Date',
                               'dg_running_min': 'DG Start Time (Minutes)',
                               'dg_running_max': 'DG End Time (Minutes)',
                               'dg_running_duration': 'DG Running Duration (Minutes)'
                               }
            if not dataset["Voltage_Current"].empty:
                voltage_related_columns = {
                    663: 'Average R Phase to Neutral Voltage (V)',
                    664: 'Average Y Phase to Neutral Voltage (V)',
                    665: 'Average B Phase to Neutral Voltage (V)',
                    666: 'Average R Phase Line Current (A)',
                    667: 'Average Y Phase Line Current (A)',
                    668: 'Average B Phase Line Current (A)'
                }
                dest = dict(column_name_map)  # or orig.copy()
                dest.update(voltage_related_columns)
                column_name_map = dest
                if not dataset["UPS_Battery_Voltage"].empty:
                    ups_battery_voltage_headers = {
                        'ups_battery_voltage_min': 'UPS Min Voltage (V)',
                        'ups_battery_voltage_max': 'UPS Max Voltage (V)'
                    }
                    dest = dict(column_name_map)  # or orig.copy()
                    dest.update(ups_battery_voltage_headers)
                    column_name_map = dest
                    if not dataset["DG_Battery_Voltage"].empty:
                        dg_battery_voltage_headers = {
                            'dg_battery_voltage_min': 'DG Min Voltage (V)',
                            'dg_battery_voltage_max': 'DG Max Voltage (V)'
                        }
                        dest = dict(column_name_map)  # or orig.copy()
                        dest.update(dg_battery_voltage_headers)
                        column_name_map = dest
                else:
                    if not dataset["DG_Battery_Voltage"].empty:
                        dg_battery_voltage_headers = {
                            'dg_battery_voltage_min': 'DG Min Voltage (V)',
                            'dg_battery_voltage_max': 'DG Max Voltage (V)'
                        }
                        dest = dict(column_name_map)  # or orig.copy()
                        dest.update(dg_battery_voltage_headers)
                        column_name_map = dest
            else:
                if not dataset["UPS_Battery_Voltage"].empty:
                    ups_battery_voltage_headers = {
                        'ups_battery_voltage_min': 'UPS Min Voltage (V)',
                        'ups_battery_voltage_max': 'UPS Max Voltage (V)'
                    }
                    dest = dict(column_name_map)  # or orig.copy()
                    dest.update(ups_battery_voltage_headers)
                    column_name_map = dest
                    if not dataset["DG_Battery_Voltage"].empty:
                        dg_battery_voltage_headers = {
                            'dg_battery_voltage_min': 'DG Min Voltage (V)',
                            'dg_battery_voltage_max': 'DG Max Voltage (V)'
                        }
                        dest = dict(column_name_map)  # or orig.copy()
                        dest.update(dg_battery_voltage_headers)
                        column_name_map = dest
                else:
                    if not dataset["DG_Battery_Voltage"].empty:
                        dg_battery_voltage_headers = {
                            'dg_battery_voltage_min': 'DG Min Voltage (V)',
                            'dg_battery_voltage_max': 'DG Max Voltage (V)'
                        }
                        dest = dict(column_name_map)  # or orig.copy()
                        dest.update(dg_battery_voltage_headers)
                        column_name_map = dest

            report_data.rename(columns=column_name_map, inplace=True)
            logger_1.debug("Report Data : {}".format(report_data))
        except Exception as e:
            logger_1.error("Merging the key columns has failed : {}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            return [report_data, report_error]  #

        report_data = report_data.round(2)
        return [report_data, report_error]

    def energy_report_generator(self, from_date, to_date, machine_id=None):
        # Extract day and time intervals separately
        from_day = from_date.date()  # Start day
        to_day = to_date.date()  # End day
        from_hour = from_date.hour  # Start hour for each day
        to_hour = to_date.hour  # End hour for each day
        # Creating an empty dictionary to store datasets pulled from Clickhouse
        dataset = dict()
        # Creating an empty dataframe to store the results of the report generation query
        report_data = None
        # Creating an error object to store errors we encounter in the report generation process
        report_error = None
        try:
            # Building the query for Energy Readings
            # Currently we are hard-coding the reading_id (509) which is the Energy Consumption reading of Energy Meter
            # Need to replace this hard coding later
            logger_1.info("Building the query for energy readings")
            params = {
                "table_name": config.table_name,
                "group_by_columns": config.group_by_columns,
                "order_by_columns": config.order_by_columns,
                "select_columns": config.select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["Energy"], energy_err_msg = self.jinja.apply_sql_template(self.general_query, params)
            err.Tracker.add_to_tracker('energy_reading_df_error', str(energy_err_msg))
            if energy_err_msg is not None:
                err.Tracker.add_to_tracker('energy_reading_df_error', str(energy_err_msg))
                raise Exception(energy_err_msg)
            else:
                logger_1.debug("Query for the energy readings : {}".format(query))
                logger_1.debug("Energy readings query result : {}".format(dataset["Energy"]))

        except Exception as e:
            logger_1.error("Querying Energy Meter Readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('energy_reading_df_error', str(e))
            return [report_data, report_error]  #

        try:
            # Building the query for Voltage and Readings Currently we are hard-coding the reading_id (663,664,
            # 665) which are the phase_wise Voltage readings (Phase to Neutral) Similarly we are hard-coding the
            # reading_id(666,667,668) which are Current readings Need to replace this hard_coding later
            params = {
                "table_name": config.voltage_table_name,
                "group_by_columns": config.voltage_group_by_columns,
                "order_by_columns": config.voltage_order_by_columns,
                "select_columns": config.voltage_select_columns,
                "from_day": str(from_day),
                "to_day": str(to_day),
                "rtu_reading_id": config.voltage_rtu_reading_id,
                "from_hour": from_hour,
                "to_hour": to_hour,
                "machine_id": machine_id
            }
            query, dataset["Voltage_Current"], vol_current_err_msg = self.jinja.apply_sql_template(self.general_query,
                                                                                                   params)
            err.Tracker.add_to_tracker('voltage_current_df_error', str(vol_current_err_msg))
            if vol_current_err_msg is not None:
                err.Tracker.add_to_tracker('voltage_current_df_error', str(vol_current_err_msg))
                raise Exception(vol_current_err_msg)
            else:
                logger_1.debug("Voltage and Current readings query  : {}".format(query))
                logger_1.debug("Voltage and Current readings query result:-{}".format(dataset["Voltage_Current"]))
        except Exception as e:
            logger_1.error("Querying Voltage and Current Readings failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('voltage_current_df_error', str(e))
            return [report_data, report_error]

        try:
            params = {
                "table_name": config.machine_details_table_name,
                "group_by_columns": None,
                "order_by_columns": None,
                "select_columns": config.machine_details_select_columns,
                "from_day": None,
                "to_day": None,
                "rtu_reading_id": None,
                "from_hour": None,
                "to_hour": None,
                "machine_id": None
            }
            query, dataset["machine_details"], machine_details_err_msg = self.jinja.apply_sql_template(
                self.general_query, params)
            err.Tracker.add_to_tracker('machine_df_error', str(machine_details_err_msg))
            if machine_details_err_msg is not None:
                raise Exception(machine_details_err_msg)
            else:
                pass
        except Exception as e:
            logger_1.error("Querying Machine Details has failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('machine_df_error', str(e))
            return [report_data, report_error]

        if (dataset["Energy"].empty or dataset["machine_details"].empty):
            logger_1.info("Empty Data set")
            return [report_data, report_error]

        try:
            # Merging the key columns (machine name, location etc)
            # report_data = report_data.merge(dataset["key_columns"], how="right", left_index=True, right_index=True)
            report_data = dataset["Energy"]
            report_data = report_data.merge(dataset["machine_details"], how="left", on="machine_id")
            err.Tracker.add_to_tracker('energy_merge_machine_error', None)
        except Exception as e:
            logger_1.error("Merging the key columns has failed : {}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('energy_merge_machine_error', str(e))
            return [report_data, report_error]  #

        # Pivot Voltage and Current
        if not dataset["Voltage_Current"].empty:
            try:
                logger_1.info("Transposing voltage and current readings")
                dataset["Voltage_Current"].set_index(['machine_id', 'rtu_id', 'day'], drop=True, inplace=True)
                report_data_voltage_current = dataset["Voltage_Current"].pivot(columns='rtu_reading_id')
                report_data_voltage_current.columns = [663, 664, 665, 666, 667, 668]
                err.Tracker.add_to_tracker('pivot_voltage_current_error', None)
            except Exception as e:
                print("Transposing Voltage and Current data has failed : {}".format(e))
                logger_1.error("Transposing Voltage and Current data has failed : {}".format(e))
                report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
                err.Tracker.add_to_tracker('pivot_voltage_current_error', str(e))
                return [report_data, report_error]  #

        # Set composite index
        try:
            print("Setting composite index on Report Data")
            logger_1.info("Setting composite index on Report Data")
            report_data['date'] = report_data['day']
            report_data['machine_id_copy'] = report_data['machine_id']
            report_data.set_index(['machine_id', 'rtu_id', 'day'], drop=True, inplace=True)
            # Combining data into report
            # Important Note: Is this the best efficiency we can get in merge?
            # TODO: Think of a better optimization to merge
            logger_1.info("Merging Energy Meter data with Voltage and Current data")
            if not dataset["Voltage_Current"].empty:
                report_data = report_data.merge(report_data_voltage_current, how="left", left_index=True,
                                                right_index=True)
            err.Tracker.add_to_tracker('setting_index_on_energy_report_error', None)
        except Exception as e:
            logger_1.error("Indexing and Merging data has failed :{}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('setting_index_on_energy_report_error', str(e))
            return [report_data, report_error]  #

        # Replacing missing values (should occur only in current)
        # But we need to verify this carefully, if any zeroes appear other than in current
        # in the final report
        logger_1.info("Filling null values in merged data")
        report_data.fillna(0, inplace=True)
        # Grouping the report on desired frequency - here the grouping is by day

        try:
            report_data["reading_name"] = "Energy Consumption"  # TODO : Remove Hardcoding later
            report_data["unit"] = "Kwh"  # TODO : Remove Hardcoding later
            report_data["energy_daily_consumption"] = report_data["energy_max"] - report_data["energy_min"]
            if not dataset["Voltage_Current"].empty:
                report_data = report_data[
                    ['machine_id_copy', 'location', 'machine_name', 'city', 'state', 'reading_name', 'unit', 'date',
                     'energy_consumption_mean', 'energy_min', 'energy_max', 'energy_daily_consumption',
                     'energy_consumption_median', 'energy_consumption_max', 'energy_consumption_min', 663, 664, 665,
                     666, 667, 668]]

            else:
                report_data = report_data[
                    ['machine_id_copy', 'location', 'machine_name', 'city', 'state', 'reading_name', 'unit', 'date',
                     'energy_consumption_mean', 'energy_min', 'energy_max', 'energy_daily_consumption',
                     'energy_consumption_median', 'energy_consumption_max', 'energy_consumption_min']]
            column_name_map = {'machine_id_copy': 'machine_id',
                               'location': 'location',
                               'machine_name': 'machine_name',
                               'city': 'city',
                               'state': 'state',
                               'reading_name': 'reading_name',
                               'unit': 'unit',
                               'date': 'Date',
                               'energy_consumption_mean': 'hourly_mean',
                               'energy_min': "from :" + str(from_date.hour) + "::0::0",
                               'energy_max': "to :" + str(to_date.hour) + "::0::0",
                               'energy_daily_consumption': 'energy_daily_consumption',
                               'energy_consumption_median': 'hourly_median',
                               'energy_consumption_max': 'hourly_max',
                               'energy_consumption_min': 'hourly_min'}
            if not dataset["Voltage_Current"].empty:
                voltage_related_columns = {
                    663: 'Average R Phase to Neutral Voltage (V)',
                    664: 'Average Y Phase to Neutral Voltage (V)',
                    665: 'Average B Phase to Neutral Voltage (V)',
                    666: 'Average R Phase Line Current (A)',
                    667: 'Average Y Phase Line Current (A)',
                    668: 'Average B Phase Line Current (A)'
                }
                dest = dict(column_name_map)  # or orig.copy()
                dest.update(voltage_related_columns)
                column_name_map = dest
            report_data.rename(columns=column_name_map, inplace=True)
            logger_1.debug("Report Data : {}".format(report_data))
            err.Tracker.add_to_tracker('merging_key_column_error', None)
        except Exception as e:
            logger_1.error("Merging the key columns has failed : {}".format(e))
            report_error = e  # TODO: Is this the best idea? Or should we create an error map locally?
            err.Tracker.add_to_tracker('merging_key_column_error', str(e))
            return [report_data, report_error]  #

        report_data = report_data.round(2)
        return [report_data, report_error]
