export interface CommandArgs {
  [key: string]: string;
}

export interface Command {
  name: string;
  args: CommandArgs | {};
  type: string;
}

export interface Thoughts {
  text: string;
  reasoning: string;
  plan: string;
  criticism: string;
  speak: string;
}
