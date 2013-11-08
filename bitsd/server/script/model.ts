export interface IEventListener {
    temperature(event: ITemperatureEvent)
    temperatureHistory(events: ITemperatureEvent[])
    message(event: IMessageEvent)
    status(event: IStatusEvent)
}

export interface IStatusEvent extends IEvent{
    status: Status;
    from: IUser;
}

export interface IEvent {
    when: Date;
}

export enum Status { closed, open }

export interface ISensor {
    id: number;
}

export interface ITemperatureEvent extends IEvent {
    temperature: number;
    sensor: ISensor;
}

export interface IUser {
    name: string;
}

export interface IMessageEvent extends IEvent {
    content: string;
    from: IUser;
}