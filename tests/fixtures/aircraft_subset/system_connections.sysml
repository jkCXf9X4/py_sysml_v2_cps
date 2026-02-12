package Aircraft {
  connect AutopilotModule.autopilotCmd to MissionComputer.autopilotInput;
  connect MissionComputer.direction_command to Environment.direction_command;
  connect Environment.orientation to AutopilotModule.currentOrientation;
  connect Environment.location to AutopilotModule.currentLocation;
  connect Environment.flight_status to AutopilotModule.feedbackBus;
}
