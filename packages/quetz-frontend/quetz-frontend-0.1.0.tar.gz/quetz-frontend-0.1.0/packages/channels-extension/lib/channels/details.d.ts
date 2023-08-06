import 'react-tabs/style/react-tabs.css';
import * as React from 'react';
declare class ChannelDetails extends React.PureComponent<any, any> {
    constructor(props: any);
    setTabIndex: (selectedTabIndex: any) => void;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<any, string | number | symbol> & {
    wrappedComponentRef?: React.Ref<ChannelDetails> | undefined;
}, any> & import("react-router").WithRouterStatics<typeof ChannelDetails>;
export default _default;
