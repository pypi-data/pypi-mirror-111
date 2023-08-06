import { ITranslator, TranslationManager } from '@jupyterlab/translation';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:translator';
})(CommandIDs || (CommandIDs = {}));
/**
 * A simplified Translator
 */
export const translator = {
    id: CommandIDs.plugin,
    autoStart: true,
    provides: ITranslator,
    activate: (app) => {
        const translationManager = new TranslationManager();
        return translationManager;
    },
};
//# sourceMappingURL=translator.js.map