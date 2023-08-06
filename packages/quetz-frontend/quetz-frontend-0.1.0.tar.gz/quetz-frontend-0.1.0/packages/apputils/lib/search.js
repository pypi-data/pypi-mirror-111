import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import * as React from 'react';
export class SearchBox extends React.PureComponent {
    constructor(props) {
        super(props);
        this.updateInput = (e) => {
            const { onTextUpdate } = this.props;
            this.setState({
                input: e.target.value,
            });
            if (onTextUpdate) {
                onTextUpdate(e.target.value);
            }
        };
        this.onSubmit = (e) => {
            const { onSubmit } = this.props;
            const { input } = this.state;
            e.preventDefault();
            if (onSubmit) {
                onSubmit(input);
            }
        };
        this.state = {
            input: '',
        };
    }
    render() {
        const { input } = this.state;
        const { onSubmit } = this.props;
        return (React.createElement("form", { onSubmit: this.onSubmit },
            React.createElement("div", { className: "btn-group" },
                React.createElement("input", { className: "input search-input", value: input, type: "text", onChange: this.updateInput, placeholder: "Search" }),
                onSubmit && (React.createElement("button", { className: "btn btn-default", type: "submit" },
                    React.createElement(FontAwesomeIcon, { icon: faSearch }))))));
    }
}
//# sourceMappingURL=search.js.map