from db_conf import Base
from sqlalchemy import Column, String, Integer


class FlowTable(Base):
    # Table's name in the db
    __tablename__ = 'flow_table'

    id = Column(Integer, primary_key=True)
    vlan_source = Column(Integer)
    ip_source = Column(String)
    firewall_node = Column(String)
    firewall_node_ip = Column(String)
    ip_destination = Column(String)
    protocol = Column(String)
    state = Column(String)
    application = Column(String)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    vlan_destination = Column(String)

    # Constructor
    def __init__(self, vlan_source, ip_source, firewall_node, firewall_node_ip, ip_destination, protocol, state,
                 application, source_port, destination_port,vlan_destination):
        self.vlan_source = vlan_source
        self.ip_source = ip_source
        self.firewall_node = firewall_node
        self.firewall_node_ip = firewall_node_ip
        self.ip_destination = ip_destination
        self.protocol = protocol
        self.state = state
        self.application = application
        self.source_port = source_port
        self.destination_port = destination_port
        self.vlan_destination = vlan_destination
