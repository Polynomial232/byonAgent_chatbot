'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class flow_page extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  flow_page.init({
    page_text: DataTypes.STRING,
    option_group: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'flow_page',
  });
  return flow_page;
};