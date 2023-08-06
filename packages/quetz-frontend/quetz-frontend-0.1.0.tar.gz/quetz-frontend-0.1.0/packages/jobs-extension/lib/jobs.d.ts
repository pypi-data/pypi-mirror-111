/// <reference types="react" />
import { ReactWidget } from '@jupyterlab/apputils';
/**
 *
 */
export declare class Jobs extends ReactWidget {
    constructor();
    _loadData(): void;
    render(): JSX.Element;
    private _data;
    private _status;
}
