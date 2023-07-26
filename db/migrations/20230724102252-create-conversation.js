"use strict"
/** @type {import('sequelize-cli').Migration} */
module.exports = {
    async up(queryInterface, Sequelize) {
        await queryInterface.createTable("conversations", {
            id: {
                allowNull: false,
                autoIncrement: true,
                primaryKey: true,
                type: Sequelize.INTEGER,
            },
            sender: {
                type: Sequelize.STRING,
            },
            receiver: {
                type: Sequelize.STRING,
            },
            message: {
                type: Sequelize.TEXT,
            },
            id_flow_page: {
                type: Sequelize.BIGINT,
                references: {
                    model: "flow_page",
                    key: "id_flow_page",
                },
            },
            id_restaurant: {
                type: Sequelize.BIGINT,
            },
            createdAt: {
                allowNull: false,
                type: Sequelize.DATE,
            },
            updatedAt: {
                allowNull: false,
                type: Sequelize.DATE,
            },
        })

        await queryInterface.addIndex("conversation", ["id_flow_page"], {
            unique: false,
            indexedDB: true,
            name: "flow_page_index",
        })
    },
    async down(queryInterface, Sequelize) {
        await queryInterface.dropTable("conversations")
    },
}
