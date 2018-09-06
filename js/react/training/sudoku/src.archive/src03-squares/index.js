import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import _ from 'lodash';

const s = 9;

function Circle(props) {
  return (
    <button className="circle" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

function Square(props) {
  return (
    <button
      className={props.class + " left" + props.col + " top" + props.row}
      onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(r, c) {
    return (
      <Square
        row={r} col={c} class="square"
        value={this.props.squares[s*r+c]}
        onClick={() => this.props.onClick(r, c)}
      />
    );
  }

  render() {
    return (
      <div>
        {_.times(s, r =>
          <div className="board-row">
            {_.times(s, c =>
              this.renderSquare(r,c)
            )}
          </div>
        )}
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      squares: Array(9*9).fill(null),
    };
  }

  renderCircle(i) {
    return <Circle value={i} />;
  }

  handleClick(r, c) {
    //alert(r+'x'+c);
    const squares = this.state.squares.slice();
    squares[s*r+c] = (squares[s*r+c] < s) ? squares[s*r+c] + 1 : 1;
    this.setState({
      squares: squares
    });
  }

  render() {
    const squares = this.state.squares;
    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={squares}
            onClick={(r, c) => this.handleClick(r, c)}
          />
        </div>
        <div className="game-nums">
          {_.times(s, i =>
            this.renderCircle(i+1)
          )}
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);
