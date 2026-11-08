from listings.models import Building

from globals import logger, log_messages


class BuldingService:
    manager = Building.objects

    def find_or_create(self, data: dict):
        query = {k: data[k] for k in ["city", "street"]}

        # 1 Parametrized queries
        building = self.manager.filter(**query).first()

        if building is None:
            building = self.manager.create(**data)

            # 5 Security logging
            logger.info(log_messages.BUILDING_SERV["create"], extra={"context": {"building_id": building.pk}})

        return building

    def update(self, building: Building, data: dict):
        # 1 Parametrized queries
        self.manager.filter(pk=building.pk).update(**data)

        # 5 Security logging
        logger.info(log_messages.BUILDING_SERV["update"], extra={"context": {"building_id": building.pk}})

    def delete(self, building: Building, data: dict):
        if building.apartments.exists():
            # 1 Parametrized queries
            self.manager.filter(pk=building.pk).update(**data)

            # 5 Security logging
            logger.info(log_messages.BUILDING_SERV["update"], extra={"context": {"building_id": building.pk}})
