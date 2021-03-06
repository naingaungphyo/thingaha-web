"""school service class for CRUD actions"""
from typing import List, Any, Optional, Dict

from sqlalchemy.exc import SQLAlchemyError

from common.data_schema import attendance_schema
from common.error import SQLCustomError, RequestDataEmpty, ValidateFail
from models.attendance import AttendanceModel
from service.service import Service


class AttendanceService(Service):
    """
    school service class for CRUD actions
    define specific params for school service in SchoolService Class
    """
    def __init__(self, logger=None) -> None:
        super().__init__(logger)

    def get_all_attendance_records(self) -> (List, Any):
        """
        get all attendance
        :return: attendance list of dict
        """
        try:
            self.logger.info("Get attendance list")
            return [attendance.attendance_dict(school, student) for attendance, school, student in AttendanceModel.get_all_attendance()]
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="GET Attendance SQL ERROR")

    def get_attendance_by_id(self, attendance_id: int) -> Optional[List]:
        """
        get attendance info by id
        :param attendance_id:
        :return: attendance list of dict
        """
        try:
            self.logger.info("get attendance info by attendance_id:{}".format(attendance_id))
            return [attendance.attendance_dict(school, student) for attendance, school, student in
                    AttendanceModel.get_attendance_by_id(attendance_id)]
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="GET Attendance by ID SQL ERROR")

    def create_attendance(self, data: Dict) -> bool:
        """
        create attendance records
        :param data:
        :return:
        """
        if not data:
            raise RequestDataEmpty("attendance data is empty")
        if not self.input_validate.validate_json(data, attendance_schema):
            self.logger.error("All attendance field input must be required.")
            raise ValidateFail("Attendance validation fail")
        try:
            return AttendanceModel.create_attendance(AttendanceModel(
                student_id=data["student_id"],
                school_id=data["school_id"],
                grade=data["grade"],
                year=data["year"],
                enrolled_date=data["enrolled_date"]))
        except SQLAlchemyError as error:
            self.logger.error("Attendance create fail. error %s", error)
            raise SQLCustomError("Attendance create fail")

    def delete_attendance_by_id(self, attendance_id: int) -> bool:
        """
        delete attendance by id
        :param attendance_id:
        :return:
        """
        try:
            self.logger.info("delete attendance info by attendance_id:{}".format(attendance_id))
            return AttendanceModel.delete_attendance_by_id(attendance_id)
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="Delete attendance by ID SQL ERROR")

    def update_attendance_by_id(self, attendance_id: int, data: Dict) -> bool:
        """
        put attendance by id
        :param attendance_id:
        :param data:
        :return:
        """
        if not data:
            raise RequestDataEmpty("school data is empty")
        if not self.input_validate.validate_json(data, attendance_schema):
            self.logger.error("All attendance field input must be required.")
            raise ValidateFail("Attendance update validation fail")
        try:
            self.logger.info("update attendance info by attendance_id:{}".format(attendance_id))
            return AttendanceModel.update_attendance(attendance_id, AttendanceModel(
                student_id=data["student_id"],
                school_id=data["school_id"],
                grade=data["grade"],
                year=data["year"],
                enrolled_date=data["enrolled_date"]))
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="Update attendance by ID SQL ERROR")
        except SQLCustomError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="No record for requested attendance")
