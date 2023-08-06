import { reduce, union } from 'lodash';
import * as React from 'react';
const BreadcrumbChild = ({ data }) => {
    if (data.link) {
        return (React.createElement("div", { className: "breadcrumb-link", 
            //@ts-ignore
            onClick: () => window.router.navigate(data.link) }, data.text));
    }
    if (data.href) {
        return (React.createElement("a", { href: data.href, className: "breadcrumb-link" }, data.text));
    }
    return data.text;
};
export class Breadcrumbs extends React.PureComponent {
    render() {
        const { items } = this.props;
        return (React.createElement("div", { className: "breadcrumbs" }, reduce(items, (unionArray, item) => union(unionArray, [
            React.createElement("div", { className: "breadcrumb-item", key: item.text },
                React.createElement(BreadcrumbChild, { data: item })),
            React.createElement("div", { className: "breadcrumb-separator", key: `${item.text}-separator` }, "\u2003/\u2003"),
        ]), []).slice(0, -1)));
    }
}
//# sourceMappingURL=breadcrumbs.js.map