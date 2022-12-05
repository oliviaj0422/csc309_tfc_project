import React from "react";


class Input extends React.Component {
    render(){
        const { value, update } = this.props;
        return (
            <>
                
                <input
                    
                    value={value}
                    onChange={event => update(event.target.value)}
                    
                />
            </>
        )
    }
}

export default Input;