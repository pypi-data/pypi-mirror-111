import { Breadcrumbs } from '@quetz-frontend/apputils';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { withRouter } from 'react-router-dom';
import 'react-tabs/style/react-tabs.css';
import * as React from 'react';
import PackageInfo from './tab-info';
import PackageMembers from './tab-members';
import PackageDetailsApiKeys from './tab-api-keys';
const PACKAGE_TABS = {
    INFO: 0,
    MEMBERS: 1,
    API_KEYS: 2,
};
const HASH_TO_INDEX = {
    info: 0,
    members: 1,
    api_keys: 2,
};
const INDEX_TO_HASH = {
    0: 'info',
    1: 'members',
    2: 'api_keys',
};
class PackageDetails extends React.PureComponent {
    constructor(props) {
        super(props);
        this.setTabIndex = (selectedTabIndex) => {
            this.setState({
                selectedTabIndex,
            });
            history.pushState(null, '', `#${INDEX_TO_HASH[selectedTabIndex]}`);
        };
        const locationHash = (window.location.hash || '#info').substring(1);
        this.state = {
            selectedTabIndex: HASH_TO_INDEX[locationHash] || PACKAGE_TABS.INFO,
        };
    }
    render() {
        const { selectedTabIndex } = this.state;
        const { match: { params: { channelId, packageId }, }, } = this.props;
        const breadcrumbItems = [
            {
                text: 'Home',
                link: '/',
            },
            {
                text: 'Channels',
                link: '/channels',
            },
            {
                text: channelId,
                link: `/channels/${channelId}`,
            },
            {
                text: 'packages',
                link: `/channels/${channelId}#packages`,
            },
            {
                text: packageId,
            },
        ];
        return (React.createElement("div", null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" },
                channelId,
                "/",
                packageId),
            React.createElement(Tabs, { selectedIndex: selectedTabIndex, onSelect: this.setTabIndex },
                React.createElement(TabList, null,
                    React.createElement(Tab, null, "Info"),
                    React.createElement(Tab, null, "Members"),
                    React.createElement(Tab, null, "API keys")),
                React.createElement(TabPanel, null,
                    React.createElement(PackageInfo, null)),
                React.createElement(TabPanel, null,
                    React.createElement(PackageMembers, { channelId: channelId, packageId: packageId })),
                React.createElement(TabPanel, null,
                    React.createElement(PackageDetailsApiKeys, { channelId: channelId, packageId: packageId })))));
    }
}
export default withRouter(PackageDetails);
//# sourceMappingURL=index.js.map