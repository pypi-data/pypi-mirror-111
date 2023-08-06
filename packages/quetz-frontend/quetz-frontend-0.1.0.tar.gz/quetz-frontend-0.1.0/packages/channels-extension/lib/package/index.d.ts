import 'react-tabs/style/react-tabs.css';
import * as React from 'react';
declare class PackageDetails extends React.PureComponent<any, any> {
    constructor(props: any);
    setTabIndex: (selectedTabIndex: any) => void;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<any, string | number | symbol> & {
    wrappedComponentRef?: React.Ref<PackageDetails> | undefined;
}, any> & import("react-router").WithRouterStatics<typeof PackageDetails>;
export default _default;
