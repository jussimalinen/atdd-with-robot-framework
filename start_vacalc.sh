RF=bin/robotframework-2.9.jar
MAIN=org.robotframework.vacalc.VacalcRunner
java -cp $RF:bin/ -Dpython.path=src $MAIN
