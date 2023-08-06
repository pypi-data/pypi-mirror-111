import { Breadcrumbs } from '@quetz-frontend/apputils';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { withRouter } from 'react-router-dom';
import 'react-tabs/style/react-tabs.css';
import * as React from 'react';
import TabInfo from './tab-info';
import ChannelDetailsPackages from './tab-packages';
import ChannelDetailsMembers from './tab-members';
import ChannelDetailsApiKeys from './tab-api-keys';
const CHANNEL_TABS = {
    INFO: 0,
    PACKAGES: 1,
    MEMBERS: 2,
    API_KEYS: 3,
};
const HASH_TO_INDEX = {
    info: 0,
    packages: 1,
    members: 2,
    api_keys: 3,
};
const INDEX_TO_HASH = {
    0: 'info',
    1: 'packages',
    2: 'members',
    3: 'api_keys',
};
class ChannelDetails extends React.PureComponent {
    constructor(props) {
        super(props);
        this.setTabIndex = (selectedTabIndex) => {
            this.setState({
                selectedTabIndex,
            });
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.delete('tab');
            // delete things from pagination
            urlParams.delete('index');
            urlParams.delete('query');
            urlParams.delete('size');
            urlParams.append('tab', INDEX_TO_HASH[selectedTabIndex]);
            history.pushState(null, '', '?' + urlParams.toString());
            // history.pushState(null, '', `#${INDEX_TO_HASH[selectedTabIndex]}`);
        };
        const urlParams = new URLSearchParams(window.location.search);
        const currentTab = urlParams.get('tab') || 'info';
        console.log('Current Tab: ', currentTab);
        this.state = {
            selectedTabIndex: HASH_TO_INDEX[currentTab] || CHANNEL_TABS.INFO,
        };
    }
    render() {
        const { selectedTabIndex } = this.state;
        const { match: { params: { channelId }, }, } = this.props;
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
            },
        ];
        return (React.createElement(React.Fragment, null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, channelId),
            React.createElement(Tabs, { selectedIndex: selectedTabIndex, onSelect: this.setTabIndex },
                React.createElement(TabList, null,
                    React.createElement(Tab, null, "Info"),
                    React.createElement(Tab, null, "Packages"),
                    React.createElement(Tab, null, "Members"),
                    React.createElement(Tab, null, "API keys")),
                React.createElement(TabPanel, null,
                    React.createElement(TabInfo, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsPackages, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsMembers, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsApiKeys, { channelId: channelId })))));
    }
}
export default withRouter(ChannelDetails);
//# sourceMappingURL=details.js.map