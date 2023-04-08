import { SNOWFLAKE_COMMAND_NAME } from '../config/Constants';

export function commandNeedsPermission(commandName) {

  return commandName !== SNOWFLAKE_COMMAND_NAME;

}
