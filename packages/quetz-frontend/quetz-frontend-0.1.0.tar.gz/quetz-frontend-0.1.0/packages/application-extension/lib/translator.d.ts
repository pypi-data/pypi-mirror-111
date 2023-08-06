import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ITranslator } from '@jupyterlab/translation';
export declare namespace CommandIDs {
    const plugin = "@quetz-frontend/application-extension:translator";
}
/**
 * A simplified Translator
 */
export declare const translator: JupyterFrontEndPlugin<ITranslator>;
