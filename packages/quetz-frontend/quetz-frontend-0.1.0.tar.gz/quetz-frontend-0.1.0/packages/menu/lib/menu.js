import { ArrayExt } from '@lumino/algorithm';
import { Panel } from '@lumino/widgets';
import { MessageLoop } from '@lumino/messaging';
/**
 * The main menu.
 */
export class MainMenu extends Panel {
    /**
     * Construct the main menu bar.
     */
    constructor() {
        super();
        /**
         * A message hook for child add/remove messages on the main area dock panel.
         *
         * @param handler
         * @param msg
         */
        this._panelChildHook = (handler, msg) => {
            switch (msg.type) {
                case 'child-added':
                    {
                        const widget = msg.child;
                        // If we already know about this widget, we're done
                        if (this._items.find((v) => v.widget === widget)) {
                            break;
                        }
                        // Otherwise, add to the end by default
                        const rank = this._items[this._items.length - 1].rank;
                        this._items.push({ widget, rank });
                    }
                    break;
                case 'child-removed':
                    {
                        const widget = msg.child;
                        ArrayExt.removeFirstWhere(this._items, (v) => v.widget === widget);
                    }
                    break;
                default:
                    break;
            }
            return true;
        };
        this._items = new Array();
        this.id = 'main-menu';
        this.addClass('topbar-item');
        MessageLoop.installMessageHook(this, this._panelChildHook);
    }
    addItem(widget, rank) {
        widget.parent = null;
        widget.addClass('topbar-item-content');
        const item = { widget, rank };
        const index = ArrayExt.upperBound(this._items, item, Private.itemCmp);
        ArrayExt.insert(this._items, index, item);
        this.insertWidget(index, widget);
    }
}
var Private;
(function (Private) {
    /**
     * A less-than comparison function for side bar rank items.
     *
     * @param first
     * @param second
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));
//# sourceMappingURL=menu.js.map