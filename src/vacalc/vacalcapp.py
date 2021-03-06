import os
import tempfile

from org.robotframework.vacalc import VacationCalculator
from vacalc.ui import VacalcFrame
from vacalc.employeestore import EmployeeStore, VacalcError
from vacalc.dateprovider import CurrentDate


class VacalcApplication(VacationCalculator):

    def create(self):
        default_db = os.path.join(tempfile.gettempdir(), 'vacalcdb.csv')
        self._db_file= os.environ.get('VACALC_DB', default_db)
        self._store = EmployeeStore(self._db_file)
        self._frame = VacalcFrame(EmployeeController(self._store), CurrentDate)
        self._frame.show()


class EmployeeController(object):

    def __init__(self, employeestore):
        self._store = employeestore
        self._change_listeners = []

    def all(self):
        return self._store.get_all_employees()

    def add(self, name, startdate):
        try:
            employee = self._store.add_employee(name, startdate)
        except VacalcError, err:
            for l in self._change_listeners:
                l.adding_employee_failed(unicode(err))
        else:
            for l in self._change_listeners:
                l.employee_added(employee)

    def add_change_listener(self, listener):
        self._change_listeners.append(listener)
