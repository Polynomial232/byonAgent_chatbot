'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class conversation extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  conversation.init({
    sender: DataTypes.STRING,
    receiver: DataTypes.STRING,
    message: DataTypes.TEXT,
    id_flow_page: DataTypes.BIGINT,
    id_restaurant: DataTypes.BIGINT
  }, {
    sequelize,
    modelName: 'conversation',
  });
  return conversation;
};