import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { Breadcrumbs, SearchBox, formatPlural } from '@quetz-frontend/apputils';
import { PaginatedList } from '@quetz-frontend/table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGlobeAmericas, faUnlockAlt, } from '@fortawesome/free-solid-svg-icons';
import ReactTooltip from 'react-tooltip';
import * as React from 'react';
class ChannelsList extends React.Component {
    constructor(props) {
        super(props);
        this.onSearch = (searchText) => {
            this.setState({ searchText });
        };
        this.state = {
            channels: null,
            searchText: '',
        };
    }
    render() {
        const { searchText } = this.state;
        const breadcrumbItems = [
            {
                text: 'Home',
                link: '/',
            },
            {
                text: 'Channels',
            },
        ];
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/paginated/channels');
        return (React.createElement(React.Fragment, null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "Channels"),
            React.createElement("div", { className: "channels-search" },
                React.createElement(SearchBox, { onTextUpdate: this.onSearch })),
            React.createElement(PaginatedList, { url: url, params: { q: searchText }, columns: getChannelsListColumns(), to: (rowData) => `/channels/${rowData.name}` })));
    }
}
export default ChannelsList;
const getChannelsListColumns = () => [
    {
        Header: '',
        accessor: 'name',
        Cell: ({ row }) => (React.createElement(React.Fragment, null,
            React.createElement("span", { "data-for": `tooltip-${row.original.name}`, "data-tip": row.original.private ? 'Private' : 'Public' },
                React.createElement(FontAwesomeIcon, { icon: row.original.private ? faUnlockAlt : faGlobeAmericas })),
            React.createElement(ReactTooltip, { id: `tooltip-${row.original.name}`, place: "right", type: "dark", effect: "solid" }))),
        width: 5,
    },
    {
        Header: '',
        accessor: 'user.profile.name',
        Cell: ({ row }) => (React.createElement("div", null,
            React.createElement("p", { className: "text" }, row.original.name),
            React.createElement("p", { className: "minor-paragraph channel-list-description" }, row.original.description))),
        width: 45,
    },
    {
        Header: '',
        accessor: 'user.username',
        Cell: ({ row }) => formatPlural(row.original.packages_count, 'package'),
        width: 35,
    },
    {
        Header: '',
        accessor: 'role',
        Cell: ({ row }) => formatPlural(row.original.packages_count, 'member'),
        width: 20,
    },
];
//# sourceMappingURL=list.js.map