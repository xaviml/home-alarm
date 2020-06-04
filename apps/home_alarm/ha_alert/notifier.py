import appdaemon.plugins.hass.hassapi as hass
from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.const import Generic, Notifier

class NotifierAlert(Alert):
  alert_id = "notifier"

  def parse_kwargs(self, kwargs) -> None:
    self.notifiers = self.get_notifiers(kwargs["notifiers"])
    self.title = kwargs.get("title", Notifier.NOTIFICATION_TITLE)
    self.message = kwargs.get("message", Notifier.NOTIFICATION_MSG)

  def get_notifiers(self, notifiers):
    return [n.replace('.', '/') for n in notifiers]

  async def alarm_fired(self, sensor_fired) -> None:
    sensor_fired_name = await self.hass.friendly_name(sensor_fired)
    for notifier in self.notifiers:
      self.hass.call_service(
        notifier,
        title=self.title + " [" + sensor_fired_name + "]",
        message="[" + sensor_fired_name + "]. " + self.message
      )
