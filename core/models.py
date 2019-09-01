from umongo import Instance, Document, fields, validate
from motor.motor_asyncio import AsyncIOMotorClient
from . import settings


class Model(Document):
    """
    Base model class extending umongo's `Document`
    """

    # Quick umongo documentation recap:
    # `Document` or `DocumentTemplate` is driver-agnostic
    # (and potentially database-agnostic, except, yeah, it's umongo)
    # data placeholder aka data schema.
    # `Instance` is driver-specific database adapter
    # `Implementation` is instance-bound version of `Document`
    # which should be used instead of original class.
    # Of course, the easy way is to define global instance
    # and wrap all models with @instance.register deco, but...
    # Approximately 50 lines below are responsible for avoiding that

    # Initialized in subclass hook
    instance = None
    implementation = None

    class Meta:
        abstract = True

    @classmethod
    def setup_instance(cls):
        if cls.instance is None:
            motor = AsyncIOMotorClient(settings.MONGO_URL)
            instance = Instance(motor.main)
            cls.instance = instance

    @classmethod
    def setup_implementation(cls):
        instance = cls.instance
        cls.implementation = instance.register(cls)

    def __init_subclass__(cls, **kwargs):
        # If implementation is being created right now:
        # Return immediately to avoid infinite recursion
        # (caused by umongo's internals)
        if cls.implementation is None: return
        cls.setup_instance()
        # Reset implementation to avoid using parent one
        cls.implementation = None
        cls.setup_implementation()

    def __new__(cls, *args, **kwargs):
        # Return implementation instead of original class
        # A-la built-in class decorator
        # (not sure if `or` is needed)
        return cls.implementation or cls


Model.setup_instance()
Model.setup_implementation()
