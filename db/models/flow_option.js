'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class flow_option extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  flow_option.init({
    groud_id: DataTypes.STRING,
    option_text: DataTypes.STRING,
    option_goto: DataTypes.STRING,
    table_name: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'flow_option',
  });
  return flow_option;
};